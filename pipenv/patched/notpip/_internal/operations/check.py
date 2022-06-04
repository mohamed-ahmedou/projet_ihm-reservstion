"""Validation of dependencies of packages
"""

import logging
from typing import TYPE_CHECKING, Callable, Dict, List, NamedTuple, Optional, Set, Tuple

from pipenv.patched.notpip._vendor.packaging.requirements import Requirement
from pipenv.patched.notpip._vendor.packaging.utils import canonicalize_name

from pipenv.patched.notpip._internal.distributions import make_distribution_for_install_requirement
from pipenv.patched.notpip._internal.metadata import get_default_environment
from pipenv.patched.notpip._internal.metadata.base import DistributionVersion
from pipenv.patched.notpip._internal.req.req_install import InstallRequirement

if TYPE_CHECKING:
    from pipenv.patched.notpip._vendor.packaging.utils import NormalizedName

logger = logging.getLogger(__name__)


class PackageDetails(NamedTuple):
    version: DistributionVersion
    dependencies: List[Requirement]


# Shorthands
PackageSet = Dict['NormalizedName', PackageDetails]
Missing = Tuple['NormalizedName', Requirement]
Conflicting = Tuple['NormalizedName', DistributionVersion, Requirement]

MissingDict = Dict['NormalizedName', List[Missing]]
ConflictingDict = Dict['NormalizedName', List[Conflicting]]
CheckResult = Tuple[MissingDict, ConflictingDict]
ConflictDetails = Tuple[PackageSet, CheckResult]


def create_package_set_from_installed() -> Tuple[PackageSet, bool]:
    """Converts a list of distributions into a PackageSet."""
    package_set = {}
    problems = False
    env = get_default_environment()
    for dist in env.iter_installed_distributions(local_only=False, skip=()):
        name = dist.canonical_name
        try:
            dependencies = list(dist.iter_dependencies())
            package_set[name] = PackageDetails(dist.version, dependencies)
        except (OSError, ValueError) as e:
            # Don't crash on unreadable or broken metadata.
            logger.warning("Error parsing requirements for %s: %s", name, e)
            problems = True
    return package_set, problems


def check_package_set(package_set, should_ignore=None):
    # type: (PackageSet, Optional[Callable[[str], bool]]) -> CheckResult
    """Check if a package set is consistent

    If should_ignore is passed, it should be a callable that takes a
    package name and returns a boolean.
    """

    missing = {}
    conflicting = {}

    for package_name, package_detail in package_set.items():
        # Info about dependencies of package_name
        missing_deps = set()  # type: Set[Missing]
        conflicting_deps = set()  # type: Set[Conflicting]

        if should_ignore and should_ignore(package_name):
            continue

        for req in package_detail.dependencies:
            name = canonicalize_name(req.name)

            # Check if it's missing
            if name not in package_set:
                missed = True
                if req.marker is not None:
                    missed = req.marker.evaluate()
                if missed:
                    missing_deps.add((name, req))
                continue

            # Check if there's a conflict
            version = package_set[name].version
            if not req.specifier.contains(version, prereleases=True):
                conflicting_deps.add((name, version, req))

        if missing_deps:
            missing[package_name] = sorted(missing_deps, key=str)
        if conflicting_deps:
            conflicting[package_name] = sorted(conflicting_deps, key=str)

    return missing, conflicting


def check_install_conflicts(to_install):
    # type: (List[InstallRequirement]) -> ConflictDetails
    """For checking if the dependency graph would be consistent after \
    installing given requirements
    """
    # Start from the current state
    package_set, _ = create_package_set_from_installed()
    # Install packages
    would_be_installed = _simulate_installation_of(to_install, package_set)

    # Only warn about directly-dependent packages; create a whitelist of them
    whitelist = _create_whitelist(would_be_installed, package_set)

    return (
        package_set,
        check_package_set(
            package_set, should_ignore=lambda name: name not in whitelist
        )
    )


def _simulate_installation_of(to_install, package_set):
    # type: (List[InstallRequirement], PackageSet) -> Set[NormalizedName]
    """Computes the version of packages after installing to_install.
    """
    # Keep track of packages that were installed
    installed = set()

    # Modify it as installing requirement_set would (assuming no errors)
    for inst_req in to_install:
        abstract_dist = make_distribution_for_install_requirement(inst_req)
        dist = abstract_dist.get_pkg_resources_distribution()

        assert dist is not None
        name = canonicalize_name(dist.project_name)
        package_set[name] = PackageDetails(dist.parsed_version, dist.requires())

        installed.add(name)

    return installed


def _create_whitelist(would_be_installed, package_set):
    # type: (Set[NormalizedName], PackageSet) -> Set[NormalizedName]
    packages_affected = set(would_be_installed)

    for package_name in package_set:
        if package_name in packages_affected:
            continue

        for req in package_set[package_name].dependencies:
            if canonicalize_name(req.name) in packages_affected:
                packages_affected.add(package_name)
                break

    return packages_affected

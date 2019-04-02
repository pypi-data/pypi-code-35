#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
class HatcherException(Exception):
    pass


class MissingFilenameError(HatcherException):
    pass


class MissingPlatformError(HatcherException):
    pass


class ChecksumMismatchError(HatcherException):
    pass


class InvalidBundle(HatcherException):
    """ Raised when a bundle file is invalid."""


class TargetFileExists(HatcherException):
    """ Raised when trying to save a file to an existing path."""


class InvalidRuntime(HatcherException):
    pass


class InvalidEgg(HatcherException):
    pass

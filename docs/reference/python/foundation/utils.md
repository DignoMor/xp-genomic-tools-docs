# `RGTools.utils`

## Purpose

Expose string conversion, reverse-complement, and JSON encoding helpers.

## Availability

Supported in release `0.1.0a2`; canonical imports are `RGTools.utils.str2bool`, `str2none`, `reverse_complement`, and `NumpyEncoder`.

## Inputs

`str2bool(value)`, `str2none(value)`, `reverse_complement(seq, mapping=...)`, and `NumpyEncoder` for `json.dumps(..., cls=NumpyEncoder)`.

## Types

`str2bool` returns bool; `str2none` returns `None` or the original string. Reverse complement accepts an iterable of mapped bases. `NumpyEncoder` handles arrays and NumPy scalar values.

## Shapes

Reverse-complement output has the same length as input. Arrays encode as JSON lists.

## Dtypes

NumPy scalars encode as Python floats; NumPy arrays encode elementwise as lists.

## Defaults

The reverse-complement map covers A/T/C/G/N in upper and lower case.

## Choices

`str2bool` treats empty, `FALSE`, and `None` tokens case-insensitively as false; all other tokens are true. `str2none` maps `NONE` case-insensitively to `None`.

## Constraints

Every reverse-complement symbol must occur in the supplied/default map.

## Outputs

Converted scalar, string/sequence, or JSON-compatible value.

## Ordering

Reverse complement reverses sequence order before mapping.

## Side effects

None.

## Failures

Unknown reverse-complement symbols raise `KeyError`; JSON unsupported values retain standard encoder failures.

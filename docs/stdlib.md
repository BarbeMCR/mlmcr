## The mlmcr Standard Library

*Notice: the standard library of mlmcr Revision 3 is __very__ bare-bones. I'm sorry for the inconvenience.*

**Table of contents:**
- [`slice`: advanced array slicing](#slice-advanced-array-slicing)

### `slice`: advanced array slicing

Opcodes defined here:
- `SLICE.FROM`: take a slice of `from` from index `start` to the end of the array and store it in `store`
  ```
  SLICE.FROM from, start, store  (from:SEQ|PSEQ|PACK, start:INT, store:->{*from})
  ```
- `SLICE.TO`: take a slice of `from` from the start of the array to `stop` and store it in `store`
  ```
  SLICE.TO from, stop, store  (from:SEQ|PSEQ|PACK, stop:INT, store:->{*from})
  ```
- `SLICE.STEP`: take a slice of `from` containing only every `step`th item and store it in `store`
  ```
  SLICE.STEP from, step, store  (from:SEQ|PSEQ|PACK, step:INT, store:->{*from})
  ```
- `SLICE.FROMTO`: take a slice of `from` from index `start` to index `stop` and store it in `store`
  ```
  SLICE.FROMTO from, start, stop, store  (from:SEQ|PSEQ|PACK, start:INT, stop:INT, store:->{*from})
  ```
- `SLICE.FROMSTEP`: take a slice of `from` from index `start` to the end of the array, containing only every `step`th item, and store it in `store`
  ```
  SLICE.FROMSTEP from, start, step, store  (from:SEQ|PSEQ|PACK, start:INT, step:INT, store:->{*from})
  ```
- `SLICE.TOSTEP`: take a slice of `from` from the start of the array to index `stop`, containing only every `step`th item, and store it in `store`
  ```
  SLICE.TOSTEP from, stop, step, store  (from:SEQ|PSEQ|PACK, stop:INT, step:INT, store:->{*from})
  ```

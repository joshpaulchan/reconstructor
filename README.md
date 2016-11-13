🖥 📸 Digitally reconstructs a photographed object.

# Installation

Make sure you have:

- Python 3.3+
- OpenCV3
- matplotlib
- numpy

and their required dependencies.

# Usage

```bash
$ python3 reconstruct.py
```

It will prompt you for the images of the object to reconstruct, so give it the path to the folder with object images.

Optionally, you can also pass the folder path in by the `i` argument.

```bash
$ python3 reconstruct.py -i './images/object/'
```

# Testing

If you'd like to develop/tweak/whatever and would like to test it, install **Pytest**.

I don't have testing set up yet lmao but if I did it would be:

```bash
$ pytest
```

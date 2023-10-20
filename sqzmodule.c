#include <Python.h>
#include "unpack.h"
#include "unpack.c"

#include "util.h"
#include "util.c"

int g_uncompressed_size;

static PyObject *method_decompress(PyObject *self, PyObject *args) {
    char *filename, *filename2 = NULL;
    int bytes_copied = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ss", &filename, &filename2)) {
        return NULL;
    }

    FILE *fp = fopen(filename, "rb");
    uint8_t *p = unpack(fp, &g_uncompressed_size);
    fclose(fp);

    FILE *fp2 = fopen(filename2, "wb");
    // bytes_copied = fputs(filename2, fp2);
    bytes_copied = fwrite(p, g_uncompressed_size, 1, fp2);
    fclose(fp2);

    return PyLong_FromLong(bytes_copied);
}

static void convert_planar_tile_4bpp(const uint8_t *src, uint8_t *dst, int dst_pitch) {
	static const int tile_h = 16;
	static const int tile_w = 16;
	static const int plane_size = 16 * (16 / 8);
	for (int y = 0; y < tile_h; ++y) {
		for (int x = 0; x < tile_w / 8; ++x) {
			for (int i = 0; i < 8; ++i) {
				const uint8_t mask = 1 << (7 - i);
				uint8_t color = 0;
				for (int b = 0; b < 4; ++b) {
					if (src[b * plane_size] & mask) {
						color |= (1 << b);
					}
				}
				if (i & 1) {
					dst[x * 4 + (i >> 1)] |= color;
				} else {
					dst[x * 4 + (i >> 1)] = color << 4;
				}
			}
			++src;
		}
		dst += dst_pitch;
	}
}

static PyObject *method_convert_planar(PyObject *self, PyObject *args) {
    // uint8_t data[16 * 8];
    uint8_t *data;
    // int bytes_copied = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "y*", &data)) {
        return NULL;
    }

    FILE *fp1 = fopen("planar_in.bin", "wb");
    fwrite(data, 128, 1, fp1);
    fclose(fp1);


    uint8_t buffer[16 * 8];
    convert_planar_tile_4bpp(data, buffer, 8);
    // memcpy(data + offset, buffer, 16 * 8);


    FILE *fp2 = fopen("planar_out.bin", "wb");
    fwrite(buffer, 128, 1, fp2);
    fclose(fp2);


    PyObject * python_val = Py_BuildValue("y#", buffer, 128);
    return python_val;

    // return PyByteArray_FromStringAndSize(buffer, 16 *8);
}

static PyMethodDef FputsMethods[] = {
    {"decompress", method_decompress, METH_VARARGS, "Python interface FUNCTION for sqz C library function"},
    {"convert_planar", method_convert_planar, METH_VARARGS, "Python interface FUNCTION for sqz C library function"},
    // {"decompress", method_decompress, METH_VARARGS, "Python interface FUNCTION for sqz C library function"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef sqzmodule = {
    PyModuleDef_HEAD_INIT,
    "sqz",
    "Python interface MODULE for the sqz C library function",
    -1,
    FputsMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_sqz(void)
{
    return PyModule_Create(&sqzmodule);
}
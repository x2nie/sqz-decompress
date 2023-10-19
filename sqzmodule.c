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

static PyMethodDef FputsMethods[] = {
    {"decompress", method_decompress, METH_VARARGS, "Python interface FUNCTION for sqz C library function"},
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
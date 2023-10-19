#include <Python.h>
#include "util.h"

static PyObject *method_decompress(PyObject *self, PyObject *args) {
    char *filename, *filename2 = NULL;
    int bytes_copied = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ss", &filename, &filename2)) {
        return NULL;
    }

    FILE *fp = fopen(filename, "rb");

    FILE *fp2 = fopen(filename2, "w");
    bytes_copied = fputs(filename2, fp2);
    fclose(fp);
    fclose(fp2);

    return PyLong_FromLong(bytes_copied);
}

static PyMethodDef FputsMethods[] = {
    {"decompress", method_decompress, METH_VARARGS, "Python interface FUNCTION for sqz C library function"},
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
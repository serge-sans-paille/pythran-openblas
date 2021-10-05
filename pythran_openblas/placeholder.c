#include <Python.h>

static PyMethodDef NoMethods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef placeholder =
{
    PyModuleDef_HEAD_INIT,
    "placeholder",     /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    NoMethods
};

PyMODINIT_FUNC PyInit_placeholder(void)
{
    return PyModule_Create(&placeholder);
}

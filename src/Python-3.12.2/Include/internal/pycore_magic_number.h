#ifndef Py_INTERNAL_MAGIC_NUMBER_H
#define Py_INTERNAL_MAGIC_NUMBER_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

/* Magic number for Python 3.12.2 (based on 3.12b1 value 3531) */
#define PYC_MAGIC_NUMBER 3531

/* This is equivalent to converting PYC_MAGIC_NUMBER to 2 bytes
   (little-endian) and then appending b'\r\n'. */
#define PYC_MAGIC_NUMBER_TOKEN \
    ((uint32_t)PYC_MAGIC_NUMBER | ((uint32_t)'\r' << 16) | ((uint32_t)'\n' << 24))

#ifdef __cplusplus
}
#endif
#endif  // !Py_INTERNAL_MAGIC_NUMBER_H

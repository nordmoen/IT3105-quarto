#include <Python.h>

typedef struct{
	const char *piece;
}QuartoPiece;

typedef struct{
	const char *board;
}QuartoBoard;

static PyObject *
parse_minimax(PyObject *self, PyObject *args)
{
	//This method will parse the python arguments into
	//C arguments so we can call our "real" minimax
	//algorithm
	
	const char *piece;
	const char *board;
	
	if(!PyArg_ParseTuple(args, "ss", &piece, &board))
		return NULL;

	QuartoPiece p;
	p.piece = piece;
	QuartoBoard b;
	b.board = board;

	return Py_BuildValue("");//Py_BuildValue("iis", x, y, next_piece.piece);
}	

static PyMethodDef MiniMaxMethods[] = {
	    {"minimax", parse_minimax, METH_VARARGS, "Calculate the best position\
		    to place a Querto piece using minimax and return the next\
			    piece to give to the opponent"},
	        {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initminimax(void)
{
	(void) Py_InitModule("querto", MiniMaxMethods);
}

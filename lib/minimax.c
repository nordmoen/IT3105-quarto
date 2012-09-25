#include <Python.h>
#include <string.h>

#define get_piece(x, y, board) board[y*4 + x]

typedef struct{
	const char *piece;
	unsigned int length;
}QuartoPiece;

typedef struct{
	QuartoPiece board[4*4];
}QuartoBoard;

int pieceEqual(QuartoPiece *a, QuartoPiece *b)
{
	int min;
	if(a->length < b->length){
		min = a->length;
	}else{
		min = b->length;
	}
	//We don't need to check the last char
	//since it will be a closing ) or ]
	for(int i = 0; i < min - 1; i++){
		//Check each part of the string
		//For instance if we have a=[D*] and b = (l*)
		//the * part will equal and we return true
		if(a->piece[i] == b->piece[i]){
			return 1;
		}
	}
	return 0;
}
void parse_board(PyObject *board, QuartoBoard *newBoard)
{
	//Board must be 4x4!
	int outer_size, inner_size = 0;
	outer_size = PyObject_Length(board);
	if(outer_size > 0){
		inner_size = PyObject_Length(PySequence_GetItem(board, 0));
	}
	if(outer_size != 4 || inner_size != 4){
		PyErr_SetString(PyExc_TypeError, "The array passed into this function\
is not a 4x4 array");
		return;
	}
	PyObject *row;
	PyObject *item;
	for(int i = 0; i < outer_size; i++){
		row = PySequence_GetItem(board, i);
		for(int j = 0; j < inner_size; j++){
			item = PySequence_GetItem(row, j);
			if(!PyString_Check(item)){
				PyErr_SetString(PyExc_TypeError, "Expected String values");
				return;
			}
			QuartoPiece p;
			p.piece = PyString_AsString(item);
			newBoard->board[i*4 + j] = p;
		}
	}
}

static PyObject *
parse_minimax(PyObject *self, PyObject *args)
{
	//This method will parse the python arguments into
	//C arguments so we can call our "real" minimax
	//algorithm
	
	const char *piece;
	PyObject *board;
	int piece_size;
	
	if(!PyArg_ParseTuple(args, "s#O", &piece, &piece_size, &board))
		return NULL;
	
	QuartoPiece p;
	p.piece = piece;
	p.length = piece_size;
	QuartoBoard b;
	parse_board(board, &b);
	if(PyErr_Occurred() != NULL){
		return NULL;
	}

	return Py_BuildValue("");//Py_BuildValue("(ii)s", x, y, next_piece.piece);
}	

static PyMethodDef MiniMaxMethods[] = {
	    {"minimax", parse_minimax, METH_VARARGS, "Calculate the best position\
		    to place a Querto piece using minimax and return the next\
			    piece to give to the opponent"},
	        {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initquarto(void)
{
	(void) Py_InitModule("quarto", MiniMaxMethods);
}

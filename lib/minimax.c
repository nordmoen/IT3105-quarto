#include <Python.h>
#include <string.h>

#define get_piece(x, y, board) board[y*4 + x]

typedef struct{
	unsigned char piece;
}QuartoPiece;

typedef struct{
	QuartoPiece board[4*4];
}QuartoBoard;

typedef struct{
	unsigned char x;
	unsigned char y;
	unsigned char next_piece;
}MinimaxRes;

void minimax(QuartoPiece *a, QuartoBoard *board, MinimaxRes *res, int max)
{

}

int pieceEqual(QuartoPiece *a, QuartoPiece *b)
{
	return ((a->piece & b->piece) > 0) || ((a->piece | b->piece) < 15);
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
			if(!PyInt_Check(item)){
				PyErr_SetString(PyExc_TypeError, "Expected Integers values");
				return;
			}
			QuartoPiece p;
			p.piece = PyInt_AsLong(item);
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
	
	unsigned char piece;
	PyObject *board;
	
	if(!PyArg_ParseTuple(args, "bO", &piece, &board))
		return NULL;
	
	QuartoPiece p;
	p.piece = piece;
	QuartoBoard b;
	parse_board(board, &b);
	if(PyErr_Occurred() != NULL){
		return NULL;
	}

	MinimaxRes result;
	minimax(&p, &b, &result, 1);

	return Py_BuildValue("(ii)i", result.x, result.y, result.next_piece);
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

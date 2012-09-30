#include <Python.h>
#include <string.h>

#define get_piece(x, y, board) board[y*4 + x]
#define set_piece(x, y, board, piece) board[y*4+x]=piece
#define max(x, y) if(x > y) x; else y;
#define min(x, y) if(x < y) x; else y;

typedef struct{
	unsigned char piece;
	unsigned char xor;
}QuartoPiece;

typedef struct{
	QuartoPiece board[4*4];
	int size;
}QuartoBoard;

typedef struct{
	unsigned char x;
	unsigned char y;
	unsigned char next_piece;
}MinimaxRes;

//Prototypes:
QuartoPiece create_piece_from_int(unsigned char val);
int is_valid_piece(QuartoPiece *piece);
int piece_equal(QuartoPiece *a, QuartoPiece *b);
int pieces_equal(QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d);
int quarto_herustic(QuartoBoard *board);

//a is the piece we want to place on the board
//board is the board filled in with some possibilities
//res is the result we want to return to the calls above
//isMax is either 1 or -1 depicting whether or not this call is a max or min call
//numPly is the ply level we are at, should decrease with one for each new call
//alpha is the alpha value
//beta is the beta value
//piecesLeft are the Quarto pieces that still have not been placed on the board
//size is the size of the above array of pieces
int minimax(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int isMax, int numPly, int alpha, int beta)
{
	//If this method always selects the last element in the piecesLeft array and
	//decrease the size with one, we don't need to create a new array each time thus saving lots
	//of calls and time
	if(numPly == 0 || board->size == 16){
		//Return the value of this end state 
		return quarto_herustic(board)*isMax;	
	}
	return 1;
}

int quarto_herustic(QuartoBoard *board)
{
	return 0;
}

QuartoPiece create_piece_from_int(unsigned char val)
{
	QuartoPiece p;
	p.piece = val;
	p.xor = val ^ 15;
	return p;
}
int is_valid_piece(QuartoPiece *piece)
{
	if(piece->piece >= 0 && piece->piece < 16){
		return 1;
	}else{
		return 0;
	}
}
int piece_equal(QuartoPiece *a, QuartoPiece *b)
{
	if(is_valid_piece(a) && is_valid_piece(b)){
		return ((a->piece & b->piece) > 0) || ((a->xor & b->xor) > 0);
	}else{
		return 0;
	}
}
int pieces_equal(QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d)
{
	if(is_valid_piece(a) && is_valid_piece(b) && is_valid_piece(c) && is_valid_piece(d)){
		return ((a->piece & b->piece & c->piece & d->piece) > 0) || 
			((a->xor & b->xor & c->xor & d->xor) > 0);
	}else{
		return 0;
	}
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
	int size = 0;
	for(int i = 0; i < outer_size; i++){
		row = PySequence_GetItem(board, i);
		for(int j = 0; j < inner_size; j++){
			item = PySequence_GetItem(row, j);
			if(item != Py_None && !PyInt_Check(item)){
				PyErr_SetString(PyExc_TypeError, "Expected Integers values or None");
				return;
			}
			if(item == Py_None){
				newBoard->board[i*4 + j] = create_piece_from_int(16);
			}else{
				unsigned char val = PyInt_AsLong(item);
				if(val <= 15 && val >= 0){
					newBoard->board[i*4 + j] = create_piece_from_int(val);
					size += 1;
				}else{
					PyErr_SetString(PyExc_ValueError, "Value is not between 0 and 15");
				}
			}
		}
	}
	newBoard->size = size;
}

void debug_print_board(QuartoBoard *board)
{
	for(int i = 0; i < 4; i++){
		printf("[");
		for(int j = 0; j < 4; j++){
			printf("%i, ", get_piece(j, i, board->board).piece);
		}
		printf("]\n");
	}
}

static PyObject *
parse_minimax(PyObject *self, PyObject *args)
{
	//This method will parse the python arguments into
	//C arguments so we can call our "real" minimax
	//algorithm
	
	unsigned char piece;
	int ply;
	PyObject *board;
	
	if(!PyArg_ParseTuple(args, "bOi", &piece, &board, &ply))
		return NULL;
	if(ply < 1){
		PyErr_SetString(PyExc_ValueError, "Ply value can not be less than 1");
		return NULL;
	}

	
	QuartoPiece p = create_piece_from_int(piece);
	QuartoBoard b;
	parse_board(board, &b);
	debug_print_board(&b);
	if(PyErr_Occurred() != NULL){
		return NULL;
	}

	MinimaxRes result;
	minimax(p, &b, &result, 1, ply, -1000, 1000);

	return Py_BuildValue(""); //Py_BuildValue("(ii)i", result.x, result.y, result.next_piece);
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

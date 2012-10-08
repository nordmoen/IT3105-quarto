#include <Python.h>
#include <string.h>

#define GET_PIECE(x, y, board1) board1[y*4 + x]
#define SET_PIECE(x, y, board1, piece) board1[y*4+x]=piece
#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

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
int quarto_herustic(QuartoBoard *board, int isMax);
int set_piece(QuartoBoard *board, int x, int y, QuartoPiece *piece);
void debug_print_board(QuartoBoard *board);
void prep_available(QuartoBoard *board, int *available);

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
	MinimaxRes r;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			if(!is_valid_piece(&GET_PIECE(j, i, board->board))){
				//We can try to place a piece here
				QuartoBoard newBoard = *board;
				if(!set_piece(&newBoard, j, i, &a)){
					PyErr_SetString(PyExc_RuntimeError, "Tried to place a piece in a position which could not be placed");
					return 0;
				}
				int re;
				if(numPly == 0 || newBoard.size == 16){
					return quarto_herustic(board, isMax);

				}else{
					int available[16];
					prep_available(&newBoard, available);
					for(int k = 0; k < 16; k++){
						if(available[k]){
							re = minimax(create_piece_from_int(k), 
									&newBoard, &r, isMax*-1, 
									numPly-1, alpha, beta);
							if(!re){
								//Something must have gone wrong 
								//longer down in the call stack
								//so just return 0 to indicate 
								//upwards that an error need to
								//be signaled to Python
								return 0;
							}
							if(isMax == 1){
								if(re > alpha){
									res->x = j;
									res->y = i;
									res->next_piece = k;
									alpha = re;
								}
								if(alpha >= beta){
									return alpha;
								}
							}else{
								if(re < beta){
									res->x = j;
									res->y = i;
									res->next_piece = k;
									beta = re;
								}
								if(alpha >= beta){
									return beta;
								}
							}
						}
					}
				}
			}
		}
	}
	if(isMax == 1){
		return alpha;
	}else{
		return beta;
	}
}
void prep_available(QuartoBoard *board, int *available)
{
	for(int i = 0; i < 16; i++){
		//Because C doesn't like to place information in a new array
		//we need to do it explicit to ensure that none of the elements
		//are 0 by default
		available[i] = 1;
	}
	QuartoPiece tmp;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			tmp = GET_PIECE(i, j, board->board);
			if(is_valid_piece(&tmp)){
				available[tmp.piece] = 0;
			}
		}
	}
}

int set_piece(QuartoBoard *board, int x, int y, QuartoPiece *piece)
{
	if(board->size < 16 && is_valid_piece(piece)){
		SET_PIECE(x, y, board->board, *piece);
		board->size += 1;
		return 1;
	}else{
		return 0;
	}
}

//This method should return a value between [1, 100] where 1 is shait and 100 is great
//board is the quarto board to evaluate and isMax is a value of either 1 or -1 to indicate
//if it is a max or min evaluation
int quarto_herustic(QuartoBoard *board, int isMax)
{
	if(board->size > 4){
		for(int i = 0; i < 4; i++){
			//Horizontal
			if(pieces_equal(&GET_PIECE(0,i, board->board), &GET_PIECE(1,i, board->board),
				&GET_PIECE(2,i, board->board), &GET_PIECE(3,i, board->board))){
				return 100*isMax;
			}
			//Vertical
			if(pieces_equal(&GET_PIECE(i,0, board->board), &GET_PIECE(i,1, board->board),
				&GET_PIECE(i,2, board->board), &GET_PIECE(i,3, board->board))){
				return 100*isMax;
			}
		}
		if(pieces_equal(&GET_PIECE(0,0, board->board),&GET_PIECE(1,1, board->board),
			&GET_PIECE(2,2, board->board), &GET_PIECE(3,3, board->board))){
			return 100*isMax;
		}
		if(pieces_equal(&GET_PIECE(0,3, board->board),&GET_PIECE(1,2, board->board),
			&GET_PIECE(2,1, board->board), &GET_PIECE(3,0, board->board))){
			return 100*isMax;
		}
		return 1;
	}else{
		//Return 1 at the moment since there can't be a win here
		//but we should try to detect smart moves, if there are three in
		//a row and so on
		return 1;
	}
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
	if(piece != NULL && piece->piece >= 0 && piece->piece < 16){
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
int parse_board(PyObject *board, QuartoBoard *newBoard)
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
		return 0;
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
				return 0;
			}
			if(item == Py_None){
				SET_PIECE(j, i, newBoard->board, create_piece_from_int(16));
			}else{
				unsigned char val = PyInt_AsLong(item);
				if(val <= 15 && val >= 0){
					SET_PIECE(j, i, newBoard->board, create_piece_from_int(val));
					size += 1;
				}else{
					PyErr_SetString(PyExc_ValueError, "Value is not between 0 and 15");
				}
			}
		}
	}
	newBoard->size = size;
	return 1;
}

void debug_print_board(QuartoBoard *board)
{
	for(int i = 0; i < 4; i++){
		printf("[");
		for(int j = 0; j < 4; j++){
			printf("%i, ", GET_PIECE(j, i, board->board).piece);
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
	if(piece < 0 || piece > 15){
		PyErr_SetString(PyExc_ValueError, "Piece is out of range for [0, 15]");
		return NULL;
	}

	
	QuartoPiece p = create_piece_from_int(piece);
	QuartoBoard b;
	if(!parse_board(board, &b)){
		return NULL;
	}

	MinimaxRes result;
	if(!minimax(p, &b, &result, 1, ply, -1000000, 1000000)){
		if(!PyErr_Occurred()){
			PyErr_SetString(PyExc_RuntimeError, "Minimax returned 0 and no error was set...");
		}
		return NULL;
	}
	if(result.x == -1 || result.y == -1){
		PyErr_SetString(PyExc_RuntimeError, "Minimax did not find any suitable xy position");
		return NULL;
	}
	return Py_BuildValue("(ii)i", result.x, result.y, result.next_piece);
}	

static PyMethodDef MiniMaxMethods[] = {
	    {"minimax", parse_minimax, METH_VARARGS, "Calculate the best position\
		    to place a Querto piece using minimax and return the next\
			    piece to give to the opponent"},
	        {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initcquarto(void)
{
	(void) Py_InitModule("cquarto", MiniMaxMethods);
}

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
int quarto_herustic(QuartoBoard *board);
int set_piece(QuartoBoard *board, int x, int y, QuartoPiece *piece);
void debug_print_board(QuartoBoard *board);
void prep_available(QuartoBoard *board, int *available);
int maxValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);
int minValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);

int minValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta)
{
	int local_beta = beta;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			if(!is_valid_piece(&GET_PIECE(j, i, board->board))){
				QuartoBoard newB = *board;
				set_piece(&newB, j, i, &a);
				int quarto_value = quarto_herustic(&newB);
				if(newB.size == 16){
					res->x = j;
					res->y = i;
					return quarto_value*(-1);
				}else if(quarto_value == 100){
					res->x = j;
					res->y = i;
					return -100;
				}else if(numPly == 0){
					if(quarto_value < local_beta){
						local_beta = quarto_value;
						res->x = j;
						res->y = i;
					}
				}else{
					int pieces_left[16]; //Array with 0 or 1 to indicate if the pieces
					//in that index is available
					prep_available(&newB, pieces_left);
					for(int k = 0; k < 16; k++){
						if(pieces_left[k]){
							MinimaxRes r;
							int value = maxValue(create_piece_from_int(k), &newB, &r, numPly-1, alpha, local_beta);
							if(value < local_beta){
								res->x = j;
								res->y = i;
								res->next_piece = k;
								local_beta = value;
							}
							if(local_beta <= alpha) return local_beta*(-1);
						}
					}
				}
			}
		}
	}
	return local_beta*(-1);
}

int maxValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta)
{
	int local_alpha = alpha;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			if(!is_valid_piece(&GET_PIECE(j, i, board->board))){
				QuartoBoard newB = *board;
				set_piece(&newB, j, i, &a);
				int quarto_value = quarto_herustic(&newB);
				if(newB.size == 16){
					res->x = j;
					res->y = i;
					return quarto_value;
				}else if(quarto_value == 100){
					res->x = j;
					res->y = i;
					return 100;
				}else if(numPly == 0){
					if(quarto_value > local_alpha){
						local_alpha = quarto_value;
						res->x = j;
						res->y = i;
					}
				}else{
					int pieces_left[16]; //Array with 0 or 1 to indicate if the pieces
					//in that index is available
					prep_available(&newB, pieces_left);
					for(int k = 0; k < 16; k++){
						if(pieces_left[k]){
							MinimaxRes r;
							int value = minValue(create_piece_from_int(k), &newB, &r, numPly-1,local_alpha, beta);
							if(value > local_alpha){
								res->x = j;
								res->y = i;
								res->next_piece = k;
								local_alpha = value;
							}
							if(local_alpha >= beta) return local_alpha;
						}
					}
				}
			}
		}
	}
	return local_alpha;
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

//This method should return a value between [0, 100] where 0 is shait and 100 is great
int quarto_herustic(QuartoBoard *board)
{
	if(board->size >= 4){
		for(int i = 0; i < 4; i++){
			//Horizontal
			if(pieces_equal(&GET_PIECE(0,i, board->board), &GET_PIECE(1,i, board->board),
				&GET_PIECE(2,i, board->board), &GET_PIECE(3,i, board->board))){
				return 100;
			}
			//Vertical
			if(pieces_equal(&GET_PIECE(i,0, board->board), &GET_PIECE(i,1, board->board),
				&GET_PIECE(i,2, board->board), &GET_PIECE(i,3, board->board))){
				return 100;
			}
		}
		if(pieces_equal(&GET_PIECE(0,0, board->board),&GET_PIECE(1,1, board->board),
			&GET_PIECE(2,2, board->board), &GET_PIECE(3,3, board->board))){
			return 100;
		}
		if(pieces_equal(&GET_PIECE(0,3, board->board),&GET_PIECE(1,2, board->board),
			&GET_PIECE(2,1, board->board), &GET_PIECE(3,0, board->board))){
			return 100;
		}
		return 0;
	}else{
		//Return 1 at the moment since there can't be a win here
		//but we should try to detect smart moves, if there are three in
		//a row and so on
		return 0;
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
	result.next_piece = -1;
	maxValue(p, &b, &result, ply, -1000000, 1000000);
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

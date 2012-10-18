#include <Python.h>
#include <string.h>
#include <minimax.h>

#define GET_PIECE(x, y, board1) board1[y*4 + x]
#define SET_PIECE(x, y, board1, piece) board1[y*4+x]=piece
#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))



int minValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta)
{
	int local_beta = beta;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			if(!is_valid_piece(&GET_PIECE(j, i, board->board))){
				QuartoBoard newB = *board;
				set_piece(&newB, j, i, &a);
				int won = quarto_win(&newB);
				if(newB.size == 16){
					//This placement filled up the board which means that
					//we can't go further down so we just update the x, j
					//and return the value of this end state
					res->x = j;
					res->y = i;
					return quarto_herustic(&newB);
				}else if(won){
					//This is the maximum we can get, which means that we won the game
					//no reason to go further down since this lead to a victory
					res->x = j;
					res->y = i;
					return -100;
				}else if(numPly == 0){
					//We have reached the bottom of the recursion
					//and we need only evaluate the possible placements
					//of the piece that we have gotten
					int quarto_value = quarto_herustic(&newB)*(-1);
					if(quarto_value < local_beta){
						local_beta = quarto_value;
						res->x = j;
						res->y = i;
					}
					if(local_beta <= alpha) return local_beta;
				}else{
					int pieces_left[16]; //Array with 0 or 1 to indicate if the pieces
					//in that index is available
					prep_available(&newB, pieces_left);
					for(int k = 0; k < 16; k++){
						if(pieces_left[k]){
							MinimaxRes r;
							int value = maxValue(create_piece_from_int(k),
								       	&newB, &r, numPly-1, 
									alpha, local_beta);
							if(value < local_beta){
								//The value we got from below is smaller
								//than the best beta we have found which
								//means we want that, so we need to update
								//x, y and update beta
								res->x = j;
								res->y = i;
								res->next_piece = k;
								local_beta = value;
							}
							//Our beta value is smaller than alpha
							//which means that the max "node" above
							//will always chose the path which leads
							//to that alpha value and there is no use
							//in recursing any more
							if(local_beta <= alpha) return local_beta;
						}
					}
				}
			}
		}
	}
	return local_beta;
}

int maxValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta)
{
	int local_alpha = alpha;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			if(!is_valid_piece(&GET_PIECE(j, i, board->board))){
				QuartoBoard newB = *board;
				set_piece(&newB, j, i, &a);
				int won = quarto_win(&newB);
				if(newB.size == 16){
					//This placement filled up the board which means that
					//we can't go further down so we just update the x, j
					//and return the value of this end state
					res->x = j;
					res->y = i;
					return quarto_herustic(&newB);
				}else if(won){
					//This is the maximum we can get, which means that we won the game
					//no reason to go further down since this lead to a victory
					res->x = j;
					res->y = i;
					return 100;
				}else if(numPly == 0){
					//We have reached the bottom of the recursion
					//and we need only evaluate the possible placements
					//of the piece that we have gotten
					int quarto_value = quarto_herustic(&newB);
					if(quarto_value > local_alpha){
						local_alpha = quarto_value;
						res->x = j;
						res->y = i;
					}
					if(local_alpha >= beta) return local_alpha;
				}else{
					int pieces_left[16]; //Array with 0 or 1 to indicate if the pieces
					//in that index is available
					prep_available(&newB, pieces_left);
					for(int k = 0; k < 16; k++){
						if(pieces_left[k]){
							MinimaxRes r;
							int value = minValue(create_piece_from_int(k), 
									&newB, &r, numPly-1,
									local_alpha, beta);
							if(value > local_alpha){
								//The value we got from below is better
								//than what we have currently found
								//which means we need to keep this
								//position and update our alpha
								res->x = j;
								res->y = i;
								res->next_piece = k;
								local_alpha = value;
							}
							//If alpha is lager than beta there is
							//no use continuing because the min node above
							//will always chose the path that lead to beta
							if(local_alpha >= beta) return local_alpha;
						}
					}
				}
			}
		}
	}
	return local_alpha;
}

int prep_available(QuartoBoard *board, int *available)
{
	for(int i = 0; i < 16; i++){
		//Because C doesn't like to place information in a new array
		//we need to do it explicit to ensure that none of the elements
		//are 0 by default
		available[i] = 1;
	}
	QuartoPiece tmp;
	int res = 16;
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			tmp = GET_PIECE(i, j, board->board);
			if(is_valid_piece(&tmp)){
				available[tmp.piece] = 0;
				res--;
			}
		}
	}
	return res;
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

int quarto_win(QuartoBoard *board)
{
	for(int i = 0; i < 4; i++){
		//Horizontal
		if(pieces_equal(&GET_PIECE(0,i, board->board), &GET_PIECE(1,i, board->board),
			&GET_PIECE(2,i, board->board), &GET_PIECE(3,i, board->board))){
			return 1;
		}
		//Vertical
		if(pieces_equal(&GET_PIECE(i,0, board->board), &GET_PIECE(i,1, board->board),
			&GET_PIECE(i,2, board->board), &GET_PIECE(i,3, board->board))){
			return 1;
		}
	}
	if(pieces_equal(&GET_PIECE(0,0, board->board),&GET_PIECE(1,1, board->board),
		&GET_PIECE(2,2, board->board), &GET_PIECE(3,3, board->board))){
		return 1;
	}
	if(pieces_equal(&GET_PIECE(0,3, board->board),&GET_PIECE(1,2, board->board),
		&GET_PIECE(2,1, board->board), &GET_PIECE(3,0, board->board))){
		return 1;
	}
	return 0;
}

//This method should return a value between [-100, 100] where -100 is shait, 0 is a draw and 100 is great
int quarto_herustic(QuartoBoard *board)
{
	if(quarto_win(board)){
		return 100;
	}
	if(quarto_gloss(board)){
	    return -100;
	}
	if(board->size==16){
	    return 0;
	}
	int value = 0;
	//update the value with different checks to arrive at a final return-value;
	value -= quarto_triple_neg(board) * 10; //We want to avoid negative situations like the plague
	//There are places where we can win, but it's far from guaranteed
	value += quarto_triple_pos(board) * 5; 
	return value;
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

int quarto_triple_pos(QuartoBoard *board)
{
	int numTrips = 0;
	int avail[16];
	int num_pieces_left = prep_available(board, avail);
	TriplePiece tp;
	for(int i = 0; i < 4; i++){
		//Horizontal
		int horiz_pieces = pieces_triple(board, &GET_PIECE(0,i, board->board), 
				&GET_PIECE(1,i, board->board), &GET_PIECE(2,i, board->board), 
				&GET_PIECE(3,i, board->board), &tp);
		if(horiz_pieces > 0){
			int diff = num_pieces_left - horiz_pieces;
			if(diff % 2 != 0){
				//Since there is an odd number of pieces which can not
				//complete the triple we found we might be able to
				//force our opponent to give us a piece which we
				//can win with
				numTrips++;
			}
		}
		//Vertical
		int vert_pieces = pieces_triple(board, &GET_PIECE(i,0, board->board), 
				&GET_PIECE(i,1, board->board), &GET_PIECE(i,2, board->board), 
				&GET_PIECE(i,3, board->board), &tp);
		if(vert_pieces > 0){
			//See logic above
			int diff = num_pieces_left - vert_pieces;
			if(diff % 2 != 0){
				numTrips++;
			}
		}
	}
	int cross_pieces = pieces_triple(board, &GET_PIECE(0,0, board->board),
			&GET_PIECE(1,1, board->board), &GET_PIECE(2,2, board->board), 
			&GET_PIECE(3,3, board->board), &tp);
	if(cross_pieces > 0){
		//See logic above
		int diff = num_pieces_left - cross_pieces;
		if(diff % 2 != 0){
			numTrips++;
		}
	}
	int cross2_pieces = pieces_triple(board, &GET_PIECE(0,3, board->board),
			&GET_PIECE(1,2, board->board), &GET_PIECE(2,1, board->board), 
			&GET_PIECE(3,0, board->board), &tp);
	if(cross2_pieces > 0){
		//See logic above
		int diff = num_pieces_left - cross2_pieces;
		if(diff % 2 != 0){
			numTrips++;
		}
	}
	return numTrips;
}

int quarto_triple_neg(QuartoBoard *board)
{
	int numTrips = 0;
	int avail[16];
	int num_pieces_left = prep_available(board, avail);
	TriplePiece tp;
	for(int i = 0; i < 4; i++){
		//Horizontal
		int horiz_pieces = pieces_triple(board, &GET_PIECE(0,i, board->board), 
				&GET_PIECE(1,i, board->board), &GET_PIECE(2,i, board->board), 
				&GET_PIECE(3,i, board->board), &tp);
		if(horiz_pieces > 0){
			int diff = num_pieces_left - horiz_pieces;
			if(diff % 2 == 0){
				//Since there are an even number of pieces which
				//will not fit into the available third spot
				//The opponent will force us to give him a winning
				//piece
				numTrips++;
			}
		}
		//Vertical
		int vert_pieces = pieces_triple(board, &GET_PIECE(i,0, board->board), 
				&GET_PIECE(i,1, board->board), &GET_PIECE(i,2, board->board), 
				&GET_PIECE(i,3, board->board), &tp);
		if(vert_pieces > 0){
			//See logic above
			int diff = num_pieces_left - vert_pieces;
			if(diff % 2 == 0){
				numTrips++;
			}
		}
	}
	int cross_pieces = pieces_triple(board, &GET_PIECE(0,0, board->board),
			&GET_PIECE(1,1, board->board), &GET_PIECE(2,2, board->board), 
			&GET_PIECE(3,3, board->board), &tp);
	if(cross_pieces > 0){
		//See logic above
		int diff = num_pieces_left - cross_pieces;
		if(diff % 2 == 0){
			numTrips++;
		}
	}
	int cross2_pieces = pieces_triple(board, &GET_PIECE(0,3, board->board),
			&GET_PIECE(1,2, board->board), &GET_PIECE(2,1, board->board), 
			&GET_PIECE(3,0, board->board), &tp);
	if(cross2_pieces > 0){
		//See logic above
		int diff = num_pieces_left - cross2_pieces;
		if(diff % 2 == 0){
			numTrips++;
		}
	}
	return numTrips;
}


int quarto_gloss(QuartoBoard *board)
{
	TriplePiece tps[10];
	int size = 0;
	for(int i = 0; i < 4; i++){
    	TriplePiece tp;
		//Horizontal
		if (pieces_triple(board, &GET_PIECE(0,i, board->board), 
		    &GET_PIECE(1,i, board->board), &GET_PIECE(2,i, board->board), 
            &GET_PIECE(3,i, board->board), &tp))
        {
            tps[size] = tp;
            size++;
        }
		//Vertical
        TriplePiece tp2;
		if (pieces_triple(board, &GET_PIECE(i,0, board->board), 
			&GET_PIECE(i,1, board->board), &GET_PIECE(i,2, board->board), 
			&GET_PIECE(i,3, board->board), &tp2))
		{
		    tps[size] = tp2;
		    size++;
		}
	}
	TriplePiece tp3;
	if (pieces_triple(board, &GET_PIECE(0,0, board->board),
		&GET_PIECE(1,1, board->board), &GET_PIECE(2,2, board->board), 
		&GET_PIECE(3,3, board->board), &tp3))
	{
	    tps[size] = tp3;
	    size++;
	}
	TriplePiece tp4;
	if (pieces_triple(board, &GET_PIECE(0,3, board->board),
		&GET_PIECE(1,2, board->board), &GET_PIECE(2,1, board->board), 
		&GET_PIECE(3,0, board->board), &tp4))
	{
	    tps[size] = tp4;
	    size++;
	}
	for(int i=0; i<size-1; i++)
	{
	    for(int j=i+1; j<size; j++)
	    {
	        QuartoPiece *a1 = tps[i].a;
	        QuartoPiece *a2 = tps[j].a;
	        QuartoPiece *b1 = tps[i].b;
	        QuartoPiece *b2 = tps[j].b;
	        QuartoPiece *c1 = tps[i].c;
	        QuartoPiece *c2 = tps[j].c;
	        int val1 = (a1->piece & b1->piece & c1->piece);
	        int val2 = (a2->piece & b2->piece & c2->piece);
	        int xor1 = (a1->xor & b1->xor & c1->xor);
	        int xor2 = (a2->xor & b2->xor & c2->xor);
	        
	        if (val1 == xor2)
	        {
	            return 1;
	        } else if (val2 == xor1)
	        {
	            return 1;
	        }
	    }
	}
	return 0;
}

int pieces_triple(QuartoBoard *board, QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d, TriplePiece *tp)
{
    int available[16];
    prep_available(board, available);
    QuartoPiece g;
    int piece_count;
    
	if(is_valid_piece(a) && is_valid_piece(b) && is_valid_piece(c) && !is_valid_piece(d)){
		if(((a->piece & b->piece & c->piece) > 0) || ((a->xor & b->xor & c->xor) > 0)){
		    piece_count=0;
		    for(int i=0; i<16; i++){
		        if(available[i]){
		            g = create_piece_from_int(i);
		            if(pieces_equal(a, b, c, (&g))){
		                piece_count++;
		            }
		        }
		    }
		    if(piece_count>0){
		        tp->a = a;
		        tp->b = b;
		        tp->c = c;
		        return piece_count;
		    }
		}
	}else if(is_valid_piece(a) && is_valid_piece(b) && !is_valid_piece(c) && is_valid_piece(d)){
		if (((a->piece & b->piece & d->piece) > 0) || ((a->xor & b->xor & d->xor) > 0)){
		    piece_count=0;
		    for(int i=0; i<16; i++){
		        if(available[i]){
		            g = create_piece_from_int(i);
		            if(pieces_equal(a, b, d, (&g))){
		                piece_count++;
		            }
		        }
		    }
		    if(piece_count>0){
                tp->a = a;
		        tp->b = b;
		        tp->c = d;
		       return piece_count;
		    }
		}
	}else if(is_valid_piece(a) && !is_valid_piece(b) && is_valid_piece(c) && is_valid_piece(d)){
		if (((a->piece & c->piece & d->piece) > 0) || ((a->xor & c->xor & d->xor) > 0)){
		    piece_count=0;
		    for(int i=0; i<16; i++){
		        if(available[i]){
		            g = create_piece_from_int(i);
		            if(pieces_equal(a, d, c, (&g))){
		                piece_count++;
		            }
		        }
		    }
		    if(piece_count>0){
                tp->a = a;
		        tp->b = c;
		        tp->c = d;
		        return piece_count;
		    }
		}
	}else if(!is_valid_piece(a) && is_valid_piece(b) && is_valid_piece(c) && is_valid_piece(d)){
		if (((d->piece & b->piece & c->piece) > 0) || ((d->xor & b->xor & c->xor) > 0)){
		    piece_count=0;
		    for(int i=0; i<16; i++){
		        if(available[i]){
		            g = create_piece_from_int(i);
		            if(pieces_equal(d, b, c, (&g))){
		                piece_count++;
		            }
		        }
		    }
		    if(piece_count>0){
                tp->a = c;
		        tp->b = b;
		        tp->c = d;
		        return piece_count;
		    }
		}
	}
	return 0;
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

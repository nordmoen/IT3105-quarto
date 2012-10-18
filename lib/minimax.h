typedef struct{
	unsigned char piece; 	//The value of the Piece
	unsigned char xor; 	//The value of the piece xored against 15 to create the compliment of the
				//Piece value to ensure that we can correctly classify the attributes
}QuartoPiece;

typedef struct{
	QuartoPiece board[4*4]; //The board with pieces
	int size;		//The number of filled in pieces
}QuartoBoard;

typedef struct{
	unsigned char x;		//The best x position found
	unsigned char y;		//The best y position found
	unsigned char next_piece;	//The best next piece to give to the opponent found
}MinimaxRes;

//This struct is used to find Triples on the board [x, x, x, y] all the xs would be in a triple
typedef struct{
    QuartoPiece *a;
    QuartoPiece *b;
    QuartoPiece *c;
}TriplePiece;

//Create a new piece from an integer type value. This is used to ensure that we
//xor the value properly
QuartoPiece create_piece_from_int(unsigned char val);
//Check if a piece is valid, only pieces with a piece value of less than 16 and larger or
//equal to 0 is valid.
int is_valid_piece(QuartoPiece *piece);
//Check if two pieces are equal each other(equality is defined as both
//having at least one attribute in common)
int piece_equal(QuartoPiece *a, QuartoPiece *b);
//Check if four pieces are equal to each other(equality is defined as all pieces
//sharing at least one attribute)
int pieces_equal(QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d);
//Check if there is a victory on the board, meaning four in a row according to
//the measure of equality outlined above. Returns 0 for no victory and 1 for victory
int quarto_win(QuartoBoard *board);
//Calculate the heuristic value of the board. Returns the value between [-100, 100]
int quarto_herustic(QuartoBoard *board);
//Set the piece on the board, returning 1 if successful and 0 otherwise
int set_piece(QuartoBoard *board, int x, int y, QuartoPiece *piece);
//Print the board in a pretty print manner
void debug_print_board(QuartoBoard *board);
//This method loops over all the pieces on the board and marking the values in
//the given input array as 0 if the pieces is on the board and 1 otherwise.
//E.g. if piece 12 is placed available[12] will be 0 and if 3 is not placed
//available[3] will be 1
int prep_available(QuartoBoard *board, int *available);
//One step of the minimax algorithm max step
int maxValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);
//One step of the minimax algorithm min step
int minValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);
//Check if any combination of the four given pieces constitutes a triple.
//The TriplePiece is then filled in with the given triples. The method returns
//the number of available pieces left which can finish the triple. The board is
//used to find the pieces not placed on the board
int pieces_triple(QuartoBoard *board, QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d, TriplePiece *tp);
//Calculate the number of losing triple combinations on the board. This method
//will find all the triples on the board and see if there is an even number of
//pieces which can complete it, if there are an even number this is a losing
//situation and we return 1 for each such situation.
int quarto_triple_neg(QuartoBoard *board);
//Calculate the number of winning triple combinations on the board. This method
//will find all the triples on the board and see if there is an odd number of
//pieces which can complete it, if there are an odd number this is a winning
//situation and we return 1 for each such situation.
int quarto_triple_pos(QuartoBoard *board);
//See if there are any guaranteed losses(gloss) on the board, this method will
//find all the triples on the board and see if any two of the have complementary
//pieces which forces the next piece to win no matter what piece it's.
//To illustrate let say we have:
//0000		1000
//0110		1101
//0011		1010
//These six pieces are placed aligned somewhere on the board, since the two
//triples have a complementary first attribute any piece given to the next
//player must finish of one of them and thus win the game.
//The method return 1 if there is such a situation and 0 if there is not
int quarto_gloss(QuartoBoard *board);

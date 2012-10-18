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

typedef struct{
    QuartoPiece *a;
    QuartoPiece *b;
    QuartoPiece *c;
}TriplePiece;

QuartoPiece create_piece_from_int(unsigned char val);
int is_valid_piece(QuartoPiece *piece);
int piece_equal(QuartoPiece *a, QuartoPiece *b);
int pieces_equal(QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d);
int quarto_win(QuartoBoard *board);
int quarto_herustic(QuartoBoard *board);
int set_piece(QuartoBoard *board, int x, int y, QuartoPiece *piece);
void debug_print_board(QuartoBoard *board);
int prep_available(QuartoBoard *board, int *available);
int maxValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);
int minValue(QuartoPiece a, QuartoBoard *board, MinimaxRes *res, int numPly, int alpha, int beta);
int pieces_triple(QuartoBoard *board, QuartoPiece *a, QuartoPiece *b, QuartoPiece *c, QuartoPiece *d, TriplePiece *tp);
int quarto_triple_neg(QuartoBoard *board);
int quarto_triple_pos(QuartoBoard *board);
int quarto_gloss(QuartoBoard *board);

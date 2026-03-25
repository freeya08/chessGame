import chess
import random

# =====================
# Model（資料層）
# =====================

# 駒の価値（評価用）
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

# 中央マス
CENTER = [chess.D4, chess.E4, chess.D5, chess.E5]


# =====================
# ViewModel（ロジック層）
# =====================


# 手の評価関数
def evaluate_move(board, move):
    score = 0

    # 駒を取る → 加点
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece is not None:
            score += PIECE_VALUES.get(captured_piece.piece_type, 0)

    # 仮想的に手を実行
    board.push(move)

    # チェックメイト → 最優先
    if board.is_checkmate():
        board.pop()
        return 100

    # チェック → 加点
    if board.is_check():
        score += 2

    # 中央制御 → 加点
    if move.to_square in CENTER:
        score += 1

    board.pop()
    return score


# 全合法手の評価一覧を作成
def get_scored_moves(board):
    moves = list(board.legal_moves)
    scored_moves = []

    for move in moves:
        score = evaluate_move(board, move)
        scored_moves.append((move, score))

    return scored_moves


# 最適手の選択
def choose_best_move(board):
    scored_moves = get_scored_moves(board)

    if not scored_moves:
        return None, [], None

    max_score = max(score for move, score in scored_moves)
    best_moves = [move for move, score in scored_moves if score == max_score]
    chosen_move = random.choice(best_moves)

    return chosen_move, scored_moves, max_score


# ヒント機能（View用のデータ生成）
def get_hint(board):
    scored_moves = get_scored_moves(board)

    if not scored_moves:
        return 0, [], None

    max_score = max(score for move, score in scored_moves)
    best_moves = [move.uci() for move, score in scored_moves if score == max_score]

    return len(scored_moves), best_moves, max_score


# 結果判定（表示用）
def get_result(board):
    result = board.result()

    if result == "1-0":
        winner = "Player (White)"
    elif result == "0-1":
        winner = "AI (Black)"
    else:
        winner = "Draw"

    if board.is_checkmate():
        reason = "Checkmate"
    else:
        reason = "Draw condition"

    return winner, reason


# =====================
# View（表示・入力）
# =====================

print("START")
print("Type 'hint' if you want move suggestions.")

board = chess.Board()

while not board.is_game_over():
    print("\nCurrent board:")
    print(board)

    while True:
        move = input("\nYour move (e2e4 / hint): ").strip()

        if move.lower() == "hint":
            count, best_moves, best_score = get_hint(board)
            print("Number of legal moves:", count)
            print("Best score:", best_score)
            print("Best moves:", best_moves)
            continue

        try:
            board.push_uci(move)
            break
        except Exception as e:
            print("invalid", e)

    if board.is_game_over():
        break

    print("\nAI thinking...")
    ai_move, _, ai_best_score = choose_best_move(board)

    if ai_move is None:
        break

    print("AI best score:", ai_best_score)
    print("AI chosen move:", ai_move.uci())

    board.push(ai_move)

print("\nGame Over")

winner, reason = get_result(board)
print("Result:", winner)
print("Reason:", reason)

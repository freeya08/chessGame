import chess
import random

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

CENTER = [chess.D4, chess.E4, chess.D5, chess.E5]


def evaluate_move(board, move):
    score = 0

    # 吃子加分
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece is not None:
            score += PIECE_VALUES.get(captured_piece.piece_type, 0)

    # 模擬走一步
    board.push(move)

    # 將死直接高分
    if board.is_checkmate():
        board.pop()
        return 100

    # 將軍加分
    if board.is_check():
        score += 2

    # 中心控制（簡化版：走到中心）
    if move.to_square in CENTER:
        score += 1

    board.pop()
    return score


def get_scored_moves(board):
    moves = list(board.legal_moves)
    scored_moves = []

    for move in moves:
        score = evaluate_move(board, move)
        scored_moves.append((move, score))

    return scored_moves


def choose_best_move(board):
    scored_moves = get_scored_moves(board)

    if not scored_moves:
        return None, [], None

    max_score = max(score for move, score in scored_moves)
    best_moves = [move for move, score in scored_moves if score == max_score]
    chosen_move = random.choice(best_moves)

    return chosen_move, scored_moves, max_score


def show_hint(board):
    scored_moves = get_scored_moves(board)

    if not scored_moves:
        print("No legal moves.")
        return

    max_score = max(score for move, score in scored_moves)
    best_moves = [move for move, score in scored_moves if score == max_score]

    # ===== 加分項 1：顯示合法手數量 =====
    print("Number of legal moves:", len(scored_moves))

    # ===== 這段是「列出所有候選手評分」的地方 =====
    # 如果之後想重新顯示全部評分，把這段註解拿掉即可
    #
    # print("\n=== Hint: Your Candidate Moves ===")
    # for move, score in scored_moves:
    #     print(f"{move.uci()}  score={score}")

    print("\n=== Suggested Best Moves ===")
    print("Best score:", max_score)
    print("Best moves:", [move.uci() for move in best_moves])


print("START")
print("Type 'hint' if you want move suggestions.")
board = chess.Board()

while not board.is_game_over():
    print("\nCurrent board:")
    print(board)

    while True:
        move = input("\nYour move (e2e4 / hint): ").strip()

        if move.lower() == "hint":
            show_hint(board)
            continue

        try:
            board.push_uci(move)
            break
        except Exception as e:
            print("invalid", e)

    if board.is_game_over():
        break

    print("\nAI thinking...")
    ai_move, ai_scored_moves, ai_best_score = choose_best_move(board)

    if ai_move is None:
        break

    # ===== 這段是「AI列出所有候選手評分」的地方 =====
    # 如果之後想重新顯示 AI 全部評分，把這段註解拿掉即可
    #
    # print("\n=== AI Candidate Moves ===")
    # for move_obj, score in ai_scored_moves:
    #     print(f"{move_obj.uci()}  score={score}")

    # ===== 加分項 2：顯示 AI 最終選擇的分數 =====
    print("AI best score:", ai_best_score)
    print("AI chosen move:", ai_move.uci())

    board.push(ai_move)

print("\nGame Over")

result = board.result()

if result == "1-0":
    print("Winner: Player (White)")
elif result == "0-1":
    print("Winner: AI (Black)")
else:
    print("Result: Draw")

if board.is_checkmate():
    print("Reason: Checkmate")
else:
    print("Reason: Draw condition")

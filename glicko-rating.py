import math

class Player:
    def __init__(self, rating, rd, vol):
        self.rating = rating
        self.rd = rd
        self.vol = vol

def g(phi):
    return 1 / math.sqrt(1 + (3 * (phi ** 2)) / (math.pi ** 2))

def E(mu, mu_j, phi_j):
    return 1 / (1 + math.exp(-g(phi_j) * (mu - mu_j)))

def update_player(player, results):
    rating = player.rating
    rd = player.rd
    vol = player.vol

    mu = (rating - 1500) / 173.7178
    phi = rd / 173.7178
    v_inv = 0
    delta = 0

    for result in results:
        opponent, outcome = result
        mu_j = (opponent.rating - 1500) / 173.7178
        phi_j = opponent.rd / 173.7178
        e = E(mu, mu_j, phi_j)

        v_inv += g(phi_j) ** 2 * e * (1 - e)
        delta += g(phi_j) * (outcome - e)

    v = 1 / v_inv
    delta *= v

    a = math.log(vol ** 2)
    tau = 0.5

    def f(x):
        ex = math.exp(x)
        return (ex * (delta ** 2 - phi ** 2 - v - ex)) / (2 * (phi ** 2 + v + ex) ** 2) - (x - a) / (tau ** 2)

    epsilon = 0.000001
    A = a
    if delta ** 2 > phi ** 2 + v:
        B = math.log(delta ** 2 - phi ** 2 - v)
    else:
        k = 1
        while f(a - k * tau) < 0:
            k += 1
        B = a - k * tau

    fA, fB = f(A), f(B)

    while abs(B - A) > epsilon:
        C = A + (A - B) * fA / (fB - fA)
        fC = f(C)
        if fC * fB < 0:
            A, fA = B, fB
        else:
            fA /= 2
        B, fB = C, fC

    new_vol = math.exp(A / 2)
    new_phi = math.sqrt(phi ** 2 + new_vol ** 2)
    new_phi_star = 1 / math.sqrt(1 / new_phi ** 2 + 1 / v)

    new_mu = mu + new_phi_star ** 2 * delta

    new_rating = 1500 + new_mu * 173.7178
    new_rd = new_phi_star * 173.7178

    player.rating = new_rating
    player.rd = new_rd
    player.vol = new_vol

    return player


def main():
    # Create two players with specific ratings, rating deviations, and volatilities
    player1 = Player(rating=1500, rd=35, vol=0.06)
    player2 = Player(rating=1500, rd=35, vol=0.06)

    # Simulate a match where player1 wins (1) and player2 loses (0)
    match_result = [(player2, 0)]  # Player1 won against player2
    player1 = update_player(player1, match_result)

    match_result = [(player1, 0)]  # Player2 lost against player1
    player2 = update_player(player2, match_result)

    # Print the new ratings, rating deviations, and volatilities
    print("Player 1:")
    print(f"New Rating: {player1.rating:.2f}")
    print(f"New RD: {player1.rd:.2f}")
    print(f"New Volatility: {player1.vol:.6f}")

    print("\nPlayer 2:")
    print(f"New Rating: {player2.rating:.2f}")
    print(f"New RD: {player2.rd:.2f}")
    print(f"New Volatility: {player2.vol:.6f}")


if __name__ == "__main__":
    main()

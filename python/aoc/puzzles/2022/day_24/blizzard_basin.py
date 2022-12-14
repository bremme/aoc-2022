# every turn all the blizzards move one position in the given direction
#     n, e, s, w

#     keep track of all blizzard positions
#     keep track of all blizzard types (n, e, s, w)
#     multiple blizzards can share the same location

#     for every posible move we need to check if we collide with a blizzard

#     max blizzards is around 3000


#     set of blizard positions can't work since non unique
#         at least blizzards with different directions can overlap
#         but not when they have the same direction
#     list of blizzards, position,


from collections import deque
from heapq import heappop, heappush

N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)


def parse(lines: list[str]):
    # find initial location of the blizzards
    valley: dict[str, set[tuple[int, int]]] = {
        "^": set(),
        ">": set(),
        "v": set(),
        "<": set(),
        "#": set(),
        # ".": set(),
    }
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == ".":
                continue
            valley[char].add((row, column))

    max_row = len(lines) - 1
    max_column = len(lines[0]) - 1

    return valley, (max_row, max_column)


class Valley:
    def __init__(self, initial_state, max_row, max_column) -> None:
        self.valley_state = {0: initial_state}
        self.max_row = max_row
        self.max_column = max_column

    def print_state(self, state):

        for row in range(self.max_row + 1):
            line = []
            for column in range(self.max_column + 1):
                for symbol in "^>v<#":
                    if (row, column) in state[symbol]:
                        line.append(symbol)
                        break
                else:
                    line.append(".")
            print("".join(line))
        print()

    def state_at_time(self, time):
        if time in self.valley_state:
            return self.valley_state[time]

        previous_state = self.valley_state[time - 1]

        next_state: dict[str, set[tuple[int, int]]] = {
            "#": previous_state["#"],
        }

        for tile_type, coordinates in previous_state.items():

            # Optimized
            if tile_type in "^v":
                # check if we need to recalculate this state
                if time >= (self.max_row - 1):
                    index = time % (self.max_row - 1)
                    next_state[tile_type] = self.valley_state[index][tile_type]
                elif tile_type == "^":
                    next_state[tile_type] = self._move_up(coordinates)
                elif tile_type == "v":
                    next_state[tile_type] = self._move_down(coordinates)
                continue

            # check if we need to recalculate this state
            if time >= (self.max_column - 1):
                index = time % (self.max_column - 1)
                next_state[tile_type] = self.valley_state[index][tile_type]
            elif tile_type == ">":
                next_state[tile_type] = self._move_right(coordinates)
            elif tile_type == "<":
                next_state[tile_type] = self._move_left(coordinates)

            # NON optimized
            # if tile_type == "^":
            #     next_state[tile_type] = self._move_up(coordinates)
            # if tile_type == "v":
            #     next_state[tile_type] = self._move_down(coordinates)

            # if tile_type == ">":
            #     next_state[tile_type] = self._move_right(coordinates)
            # if tile_type == "<":
            #     next_state[tile_type] = self._move_left(coordinates)

        self.valley_state[time] = next_state

        # print(f"start at {time}:")
        # self.print_state(next_state)
        return next_state

    def _move_up(self, coordinates):
        return self._move(coordinates, -1, 0)

    def _move_right(self, coordinates):
        return self._move(coordinates, 0, 1)

    def _move_down(self, coordinates):
        return self._move(coordinates, 1, 0)

    def _move_left(self, coordinates):
        return self._move(coordinates, 0, -1)

    def _move(self, coordinates, delta_row, delta_column):
        new_coordinates = [None] * len(coordinates)

        for index, (row, column) in enumerate(coordinates):

            new_row, new_column = (row + delta_row, column + delta_column)

            if new_row == 0:
                new_row = self.max_row - 1

            if new_row == self.max_row:
                new_row = 1

            if new_column == 0:
                new_column = self.max_column - 1

            if new_column == self.max_column:
                new_column = 1

            new_coordinates[index] = new_row, new_column

        return set(new_coordinates)


def determine_next_positions(position, valley_state, max_rows):

    # try moving N, E, S, W or stay
    for move in [N, E, S, W, (0, 0)]:
        posible_next_position = position[0] + move[0], position[1] + move[1]

        if posible_next_position in valley_state["^"]:
            continue
        if posible_next_position in valley_state[">"]:
            continue
        if posible_next_position in valley_state["v"]:
            continue
        if posible_next_position in valley_state["<"]:
            continue
        if posible_next_position in valley_state["#"]:
            continue

        if posible_next_position[0] == -1:
            continue

        if posible_next_position[0] == (max_rows + 1):
            continue

        yield posible_next_position


def solve_bfs(start, end, valley: Valley, global_time_offset=0):

    visited = set()

    queue: deque = deque()

    queue.append((0, start[0], start[1]))

    print(f"start = {start}, end = {end}")

    while queue:

        time, row, column = queue.popleft()

        if (time, row, column) in visited:
            continue

        visited.add((time, row, column))

        # get next valley state
        next_valley_state = valley.state_at_time(time + 1 + global_time_offset)

        # determine where to go next
        for new_row, new_column in determine_next_positions(
            (row, column), next_valley_state, valley.max_row
        ):
            # we found the exit
            if (new_row, new_column) == end:
                return time + 1

            queue.append((time + 1, new_row, new_column))


def solve_dijkstra(start, end, valley: Valley):

    heap = []

    visited = set()

    heappush(heap, (0, start[0], start[1]))

    print(f"start = {start}, end = {end}")

    while heap:
        time, row, column = heappop(heap)

        if (row, column, time) in visited:
            continue

        visited.add((row, column, time))

        # get next valley state
        next_valley_state = valley.state_at_time(time + 1)

        # determine where to go next
        for new_row, new_column in determine_next_positions(
            (row, column), next_valley_state, valley.max_row
        ):
            # we found the exit
            if (new_row, new_column) == end:
                return time + 1

            heappush(heap, (time + 1, new_row, new_column))

    return None


def solve_part_one(lines: list[str], example: bool) -> int:
    state, (max_row, max_column) = parse(lines)

    start = (0, 1)
    end = (max_row, max_column - 1)

    valley = Valley(initial_state=state, max_row=max_row, max_column=max_column)

    valley.print_state(state)

    # return solve_dijkstra(start=start, end=end, valley=valley)

    return solve_bfs(start=start, end=end, valley=valley)


def solve_part_two(lines: list[str], example: bool) -> int:
    state, (max_row, max_column) = parse(lines)

    start = (0, 1)
    end = (max_row, max_column - 1)

    valley = Valley(initial_state=state, max_row=max_row, max_column=max_column)

    first_trip = solve_bfs(start=start, end=end, valley=valley)
    print(f"first_trip = {first_trip}")
    # breakpoint()

    trip_back = solve_bfs(
        start=end, end=start, valley=valley, global_time_offset=first_trip
    )
    print(f"trip_back = {trip_back}")

    trip_back_to_goal = solve_bfs(
        start=start, end=end, valley=valley, global_time_offset=trip_back + first_trip
    )
    print(f"trip_back_to_goal = {trip_back_to_goal}")

    return first_trip + trip_back + trip_back_to_goal

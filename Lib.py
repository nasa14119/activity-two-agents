import ast
import csv
from pathlib import Path

import flask
import numpy as np
import pandas as pd

app = flask.Flask(__name__)
BASE = Path(__file__).resolve().parent
tmax = 10


def load_nodes():
    nodes = {}
    with open(BASE / "Nodes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            point = tuple(float(v) for v in ast.literal_eval(row["Points"]))
            nodes[int(row["Node"])] = {
                "node": int(row["Node"]),
                "point": point,
                "dirt": int(row["Dirt"]),
            }
    return nodes


def load_routes():
    routes = {}
    with open(BASE / "Routes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            agent = int(row["Agent"])
            routes.setdefault(agent, []).append(int(row["Node"]))
    return routes


@app.route("/")
def index():
    return flask.render_template("index.html", tmax=tmax)


@app.route("/api/data")
def data():
    return flask.jsonify({"nodes": load_nodes(), "routes": load_routes()})


def ZigZag(id, matrix, df):
    right = True
    rows = matrix.shape[0]
    res = []
    if matrix[0][0] != 1:
        res.append([id, 1])
    for col in range(rows):
        curr = []
        for c in matrix[col]:
            curr.append([id, c])
        if not right:
            curr = reversed(curr)
        res = [*res, *curr]
        right = not right
    res.append([id, 1])
    df = pd.concat([df, pd.DataFrame(res, columns=df.columns)])
    return df


def Spiral(id, matrix, df):
    res = []
    right = True
    isFirst = matrix[0][0] == 1
    while True:
        cur = []
        if right:
            cur = matrix[0, :]
            matrix = matrix[1:, :]
        else:
            cur = matrix[-1, :]
            cur = reversed(cur)
            matrix = matrix[:-1, :]
        res = [*res, *cur]
        if matrix.shape[0] < 1:
            break
        if not right:
            cur = matrix[:, 0]
            cur = reversed(cur)
            matrix = matrix[:, 1:]
        else:
            cur = matrix[:, -1]
            matrix = matrix[:, :-1]
        res = [*res, *cur]
        right = not right

    res = [[id, val] for val in res]
    if not isFirst:
        res = [[id, 1], *res]
    res.append([id, 1])
    df = pd.concat([df, pd.DataFrame(res, columns=df.columns)])
    return df


def Ran(id, matrix, df):
    res = []
    if matrix[0][0] != 1:
        res.append([id, 1])
    S = np.zeros((matrix.size, matrix.size))
    i, j = matrix.shape
    for m in range(i):
        for n in range(j):
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue
                    try:
                        matrix[m + x, n + y]
                        S[
                            np.ravel_multi_index([m, n], matrix.shape),
                            np.ravel_multi_index([m + x, n + y], matrix.shape),
                        ] = 1
                    except:  # noqa: S112, E722
                        continue
    pos = matrix[0][0]
    for _ in range(np.random.randint(10, 31)):
        pos = np.random.choice(np.where(S[pos, :] != 0)[0])
        x, y = np.unravel_index(pos, matrix.shape)
        res.append([id, matrix[x][y]])
    res.append([id, 1])
    df = pd.concat([df, pd.DataFrame(res, columns=df.columns)])
    return df


def Parameters(Options):
    METHODS = ["zig", "ran", "spi"]
    if Options.Method not in METHODS:
        Options.Method = "zig"
    if not Options.Columns:
        Options.Columns = 8
    if not Options.Rows:
        Options.Rows = 8
    method = {"zig": ZigZag, "spi": Spiral, "ran": Ran}[Options.Method]
    agents = Options.Agents
    DF = pd.DataFrame(columns=["Agent", "Node"])
    row, column = Options.Rows, Options.Columns
    matrix = np.arange(1, row * column + 1).reshape(row, column).T
    for agent, mat in enumerate(np.array_split(matrix, agents)):
        DF = method(agent + 1, mat, DF)

    DN = pd.DataFrame(columns=["Node", "Points", "Dirt"])
    p = Options.Persentil
    dirty_matrix = np.random.binomial(1, p, (row, column))
    i = 0
    for y in range(row):
        for x in range(column):
            i += 1
            DN = pd.concat(
                [
                    DN,
                    pd.DataFrame(
                        [[i, f"({x},{y},0)", dirty_matrix[y][x]]], columns=DN.columns
                    ),
                ]
            )
    DN.to_csv("Nodes.csv", index=False)
    DF.to_csv("Routes.csv", index=False)


def Sim(Options):
    global tmax
    tmax = Options.Tmax
    app.run(debug=True)

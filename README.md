# Activity 2

This is a simulation of agents trying to clean a room

## Requirements

- Python >= 3.13
- venv is prefered

> [!NOTE]
> This project was using the uv package manager not tested with conda
> the `requirements.txt` is provided for support to other managers.

## Install

```bash
git clone https://github.com/nasa14119/activity-two-agents
```

create a venv with the tool of your chousing

### install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
uv sync
```

## Commands

To run the project run:

```bash
python Main.py <COMMAND>
```

The main command are `Main.py Sim` and `Main.py Parameters`

### Sim

| Command     | Description                                                                  |
| ----------- | ---------------------------------------------------------------------------- |
| `--help -h` | Show available commands and details                                          |
| `--Tmax`    | Default to 10s is the maximum time that the agents have to complete the task |

### Parameters

| Command                 | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| `--help -h`             | Show available command and descriptions of them                          |
| `--Method METHOD`       | Movement method: zigsag=zig random=ran spiral=spi (deafult=zig)          |
| `--Columns COLUMNS`     | Columns of the matrix (default=8)                                        |
| `--Rows ROWS`           | Rows of the matrix (default=8)                                           |
| `--Agents AGENTS`       | Agents you whant to add to your simulation (default=1)                   |
| `--Persentil PERSENTIL` | Define the percentil of dirty cells in the grid from 0 to 1 defaults=0.5 |

intervalId = 0;
class LifeArgs {
    // 构造函数，用于初始化新创建的对象
    constructor(width, height, frequency, density) {
        this.gridSize = 10;
        this.width = Math.floor(width / 10);
        this.height = Math.floor(height / 10);
        this.frequency = frequency;
        this.density = density;
    }
}

function stop_life() {
    if (intervalId != 0) {
        clearInterval(intervalId);
        intervalId = 0;
    }

}

function clear_life() {
    stop_life();
    var canvas = document.getElementById("life-canvas");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
function get_args() {
    var canvas = document.getElementById("life-canvas");
    width = canvas.width
    height = canvas.height;
    frequency = document.getElementById("frequency").value;
    density = document.getElementById("density").value;
    const args = new LifeArgs(width, height, frequency, density);
    return args;
}
function start_life() {
    var args = get_args();
    let cells = Array.from({ length: args.height }, () => Array(args.width).fill(0))
    init_cells(cells, args);

    draw_cells(cells, args);
    interval = Math.floor(1000 / args.frequency);
    intervalId = setInterval(function () {
        next_generation(cells, args);
        draw_cells(cells, args);
    }, interval);

}

function init_cells(cells, args) {
    let blackNum = Math.floor(args.width * args.height * args.density / 100);
    for (let i = 0; i < blackNum; i++) {
        let x = Math.floor(Math.random() * (args.width - 1));
        let y = Math.floor(Math.random() * (args.height - 1));
        cells[y][x] = 1;
    }
}

function draw_cells(cells, args) {
    var canvas = document.getElementById("life-canvas");

    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // 设置方格的参数
    var gridSize = args.gridSize; // 每个方格的大小

    // 绘制方格
    for (var row = 0; row < args.height; row++) {
        for (var col = 0; col < args.width; col++) {
            // 绘制方格边框（可选，如果你想要看到方格线）
            ctx.strokeRect(col * gridSize, row * gridSize, gridSize, gridSize);

            // 随机决定是否绘制黑色小方块
            if (cells[row][col] === 1) {
                ctx.fillStyle = "black";
                ctx.fillRect((col * gridSize) + 1, (row * gridSize) + 1, gridSize - 2, gridSize - 2);
            }
        }
    }
}

function next_generation(cells, args) {
    let nextCells = Array.from({ length: args.height }, () => Array(args.width).fill(0))
    for (let row = 0; row < cells.length; row++) {
        for (let col = 0; col < cells[0].length; col++) {
            nextCells[row][col] = getNextStatus(cells, row, col);
        }
    }
    for (let row = 0; row < cells.length; row++) {
        for (let col = 0; col < cells[0].length; col++) {
            cells[row][col] = nextCells[row][col]
        }
    }

}
// 如果一个细胞为存活，邻居中少于两个为存活，它变为死亡。（模拟生命数量过少）
// 如果一个细胞为存活，邻居中有两个或3个为存活，它保持为存活。
// 如果一个细胞为存活，邻居中超过3个为存活，它变为死亡。（模拟生命数量过多）
// 如果一个细胞为死亡，邻居中恰好有3个为存活，它变为存活。（模拟繁殖）
function getNextStatus(cells, row, col) {
    let neighborNum = getNeighborsNum(cells, row, col);
    if (cells[row][col] === 1) {
        if (neighborNum < 2) {
            return 0;
        } else if (neighborNum === 2 || neighborNum === 3) {
            return 1;
        } else {
            return 0;
        }
    } else {
        if (neighborNum === 3) {
            return 1;
        } else {
            return 0;
        }
    }

}

function getNeighborsNum(cells, row, col) {
    let i1 = row - 1;
    if (i1 < 0) {
        i1 = 0;
    }
    let i2 = row + 1;
    if (i2 === cells.length) {
        i2 = cells.length - 1;
    }
    let j1 = col - 1;
    if (j1 < 0) {
        j1 = 0;
    }
    let j2 = col + 1;
    if (j2 === cells[0].length) {
        j2 = cells[0].length - 1;
    }
    let num = 0;
    for (let i = i1; i <= i2; i++) {
        for (let j = j1; j <= j2; j++) {
            if (cells[i][j] === 1) {
                num += 1;
            }
        }
    }
    if (cells[row][col] === 1) {
        num -= 1;
    }

    return num;
}
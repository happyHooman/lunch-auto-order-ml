const w = document.getElementsByTagName('iframe')[0].contentWindow;


w.Units.prototype.update_number = function (i, v) {
    w.$('#input_' + this.number + '_' + i).val(v);
    this.get_num(0, i);
    this.change_one_input2(w.document.querySelector('#input_' + this.number + '_' + i), 0, i);
};

w.Units.prototype.reduceUnit = function (i, step) {
    const initial = this.qq[i];
    while (this.xxx !== 0 && this.qq[i] >= step) {
        this.update_number(i, this.qq[i] - step);
        w.rashet();
    }
    if (this.xxx === 0) {
        this.update_number(i, this.qq[i] + step);
    }
    w.rashet();
    return initial === this.qq[i];
};

w.Units.prototype.reduce = function (step) {
    console.log('reduce')
    let changed = false;
    for (let i = 5; i > 0; i--) {
        changed = this.reduceUnit(i, step) || changed;
    }
    return changed;
};

w.Units.prototype.roundUnits = function (step, down = true) {
    let changed = false;
    for (let i = 1; i < 8; i++) {
        if (this.qq[i] % step !== 0) {
            const init = this.qq[i];
            if (down) {
                this.update_number(i, Math.floor(this.qq[i] / step) * step);
                w.rashet();
                if (this.xxx === 0) {
                    this.update_number(i, init);
                    w.rashet();
                    continue;
                }
                changed = true;
            } else {
                const num = Math.ceil(this.qq[i] / step) * step;
                if (num > this.maxUnits[i]) continue;
                this.update_number(i, num);
                changed = true;
            }
            w.rashet();
        }
    }
    return changed;
};

w.Units.prototype.replaceUnits = function (first, second, step) {
    const salary = [.2, .8, 1.2, 1.4, 1.8, 12.2, .2, 7.8];
    const before = [this.qq[first], this.qq[second]];
    let initial;
    let leftRevivals;

    do {
        if (this.qq[second] === this.maxUnits[second] || this.qq[first] === 0) return false;
        if (this.qq[first] < step) step = this.qq[first];

        leftRevivals = this.xxx;
        initial = [this.qq[first], this.qq[second]];
        let first_units_number = this.qq[first] - step;
        let second_units_number = this.qq[second] + Math.floor(step * salary[first] / salary[second]);
        console.log(`-${first_units_number} from ${first}, +${second_units_number} to ${second}`);

        if (second_units_number > this.maxUnits[second]) {
            console.log('second units to max');
            second_units_number = this.maxUnits[second];
            first_units_number = this.qq[first] - Math.floor((this.maxUnits[second] - this.qq[second]) * salary[second] / salary[first]);
        }

        this.update_number(first, first_units_number);
        this.update_number(second, second_units_number);
        w.rashet();

    } while (this.xxx > leftRevivals && this.qq[first] > 0);

    if (this.xxx < leftRevivals) {
        console.log('revert last');
        console.log(this.xxx, '<', leftRevivals);
        this.update_number(first, initial[0]);
        this.update_number(second, initial[1]);
    }
    this.roundUnits(step);
    w.rashet();
    return this.qq[first] === before[0] && this.qq[second] === before[1];
};

w.Units.prototype.replace = function (step) {
    console.log('replace');
    let changed = false;
    for (let i = 1; i < 8; i++) {
        for (let j = 1; j < 8; j++) {
            if (i === j) continue;
            changed = this.replaceUnits(i, j, step) || changed;
        }
    }
    return changed;
};

w.Units.prototype.salary = function () {
    const salary = [.1, .4, .6, .7, .9, 6.9, .1, 3.9];
    let c = 0;
    for (let i = 0; i < 8; i++) {
        c += this.qq[i] * salary[i];
    }
    return c;
};

w.Units.prototype.optimize = function (step = 1000) {
    this.maxUnits = [...this.qq];
    console.log('initial salary', this.salary());
    w.rashet();

    let changed;
    do {
        const reduced = this.reduce(step);
        const replaced = this.replace(step);
        const rounded = this.roundUnits(step, false);
        changed = reduced || replaced || rounded;
    } while (!changed);
    this.reduce(step);


    console.log('final salary', this.salary());
};

function op() {
    w.unitu[0].optimize()
}

const p = w.document.querySelector('#army_0 .title_unit span');
const bt = document.createElement('button');
bt.innerText = 'optimize';
bt.onclick = op;
p.prepend(bt);
// const se = document.createElement()
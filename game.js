'use strict';

function rashet() {
    console.log('rashet');
}

const unitu = [{
    qq: [0, 0, 0, 0, 0, 0, 0, 0],
    xxx: 10,
    get_num(n, m) {
        console.log('num', n, m);
    },
    change_one_input2(selector, n, m) {
        console.log(selector, n, m);
    }
}];

// ==============
let maxUnits = [...unitu[0].qq];

function update_number(i, v) {
    $('#input_0_' + i).val(v);
    unitu[0].get_num(0, i);
    unitu[0].change_one_input2(document.querySelector('#input_0_' + i), 0, i);
}

function reduceUnit(i, step) {
    const initial = unitu[0].qq[i];
    while (unitu[0].xxx !== 0 && unitu[0].qq[i] >= step) {
        update_number(i, unitu[0].qq[i] - step);
        rashet();
    }
    if (unitu[0].xxx === 0) {
        update_number(i, unitu[0].qq[i] + step);
    }
    rashet();
    return initial === unitu[0].qq[i];
}

function reduce(step) {
    console.log('reduce')
    let changed = false;
    for (let i = 5; i > 0; i--) {
        changed = reduceUnit(i, step) || changed;
    }
    return changed;
}

function roundUnits(step, down = true) {
    let changed = false;
    for (let i = 1; i < 8; i++) {
        if (unitu[0].qq[i] % step !== 0) {
            const init = unitu[0].qq[i];
            if (down) {
                update_number(i, Math.floor(unitu[0].qq[i] / step) * step);
                rashet();
                if (unitu[0].xxx === 0) {
                    update_number(i, init);
                    continue;
                }
                changed = true;
            } else {
                const num = Math.ceil(unitu[0].qq[i] / step) * step;
                if (num > maxUnits[i]) continue;
                update_number(i, num);
                changed = true;
            }
            rashet();
        }
    }
    return changed;
}

function replaceUnits(first, second, step) {
    const salary = [.1, .4, .6, .7, .9, 6.9, .1, 3.9];
    const before = [unitu[0].qq[first], unitu[0].qq[second]];
    let initial;
    let leftRevivals;

    do {
        if (unitu[0].qq[second] === maxUnits[second] || unitu[0].qq[first] === 0) return false;
        if (unitu[0].qq[first] < step) step = unitu[0].qq[first];

        leftRevivals = unitu[0].xxx;
        initial = [unitu[0].qq[first], unitu[0].qq[second]];
        let first_units_number = unitu[0].qq[first] - step;
        let second_units_number = unitu[0].qq[second] + Math.floor(step * salary[first] / salary[second]);
        console.log(`-${first_units_number} from ${first}, +${second_units_number} to ${second}`);

        if (second_units_number > maxUnits[second]) {
            console.log('second units to max');
            second_units_number = maxUnits[second];
            first_units_number = unitu[0].qq[first] - Math.floor((maxUnits[second] - unitu[0].qq[second]) * salary[second] / salary[first]);
        }

        update_number(first, first_units_number);
        update_number(second, second_units_number);
        rashet();

    } while (unitu[0].xxx > leftRevivals && unitu[0].qq[first] > 0);

    if (unitu[0].xxx < leftRevivals) {
        console.log('revert last');
        console.log(unitu[0].xxx, '<', leftRevivals);
        update_number(first, initial[0]);
        update_number(second, initial[1]);
    }
    roundUnits(step);
    rashet();
    return unitu[0].qq[first] === before[0] && unitu[0].qq[second] === before[1];
}

function replace(step) {
    console.log('replace')
    let changed = false;
    for (let i = 1; i < 8; i++) {
        for (let j = 1; j < 8; j++) {
            if (i === j) continue;
            changed = replaceUnits(i, j, step) || changed;
        }
    }
    return changed;
}

function cost() {
    const salary = [.1, .4, .6, .7, .9, 6.9, .1, 3.9];
    let c = 0;
    for (let i = 0; i < 8; i++) {
        c += unitu[0].qq[i] * salary[i];
    }
    return c;
}

function optimize(step = 1000) {
    maxUnits = [...unitu[0].qq];
    console.log('initial cost', cost());
    rashet();

    let changed;
    do {
        const reduced = reduce(step);
        const replaced = replace(step);
        const rounded = roundUnits(1000, false);
        changed = reduced || replaced || rounded;
    } while (!changed);

    reduce(step);

    console.log('final cost', cost());
}

// ==========================

optimize();

replace(1, 2, 1000)
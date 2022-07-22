let current_set;
let current_list;
var index;
var collectedMoons = [];
var undo_list = [];

let story_advance = document.getElementById("advance_set");
let kingdom_advance = document.getElementById("advance_kingdom");
let undo_btn = document.getElementById("undo_btn");

function initialize() {
    current_list = moonData[0]['moons']; // Set moon list to cascade.
    current_set = 0;
    redefine_seed();
}

function redefine_seed() {
    index = 3;
    undo_list = [];
    undo_btn.style.display = 'none';
    document.getElementById("moon1").innerHTML = current_list[0]['name'] + "<b>" + current_list[0]['trait'] + "</b>";
    collectedMoons.push(current_list[0]['id']);
    document.getElementById("moon2").innerHTML = current_list[1]['name'] + "<b>" + current_list[1]['trait'] + "</b>";
    collectedMoons.push(current_list[1]['id']);
    document.getElementById("moon3").innerHTML = current_list[2]['name'] + "<b>" + current_list[2]['trait'] + "</b>";
    collectedMoons.push(current_list[2]['id']);
}

function generate_new_moon(moonid) {
    if (index >= current_list.length) { return; }
    if (undo_list.length == 0) { undo_btn.style.display = 'inline'; }
    undo_list.push({
        "action": "moon",
        "id": moonid,
        "prior_data": document.getElementById(moonid).innerHTML
    });

    moon = current_list[index];
    index++;
    if (collectedMoons.includes(moon['id'])) { generate_new_moon(moonid); }
    document.getElementById(moonid).innerHTML = moon['name'] + "<b>" + moon['trait'] + "</b>";
    collectedMoons.push(moon['id']);
}

function handleKeyPress(e) {
    if (e.code == "KeyZ") {
        e.preventDefault();
        undo_last();
    }
    else if (e.code == "Digit1") {
        generate_new_moon("moon1");
    }
    else if (e.code == "Digit2") {
        generate_new_moon("moon2");
    }
    else if (e.code == "Digit3") {
        generate_new_moon("moon3");
    }
}

function next_kingdom() {
    current_set++;
    while (moonData[current_set]['set'].slice(-1) != "1") {
        current_set++;
    }
    document.getElementById('kingdom_header').innerHTML = moonData[current_set]['set'].slice(0, -2);
    if (moonData[current_set]['transition_moon'] == null) {
        story_advance.style.display = 'none';
    }
    else {
        story_advance.style.display = 'inline';
        story_advance.innerHTML = "Got " + moonData[current_set]['transition_moon'];
    }

    if (current_set + 1 >= moonData.length) { kingdom_advance.style.display = 'none'; }

    current_list = moonData[current_set]['moons'];
    redefine_seed();
}

function advance_set() {
    current_set++;
    current_list = moonData[current_set]['moons'];
    index = 0;
    if (moonData[current_set]['transition_moon'] == null) {
        story_advance.style.display = 'none';
    }
    else {
        story_advance.style.display = 'inline';
        story_advance.innerHTML = "Got " + moonData[current_set]['transition_moon'];
    }
}

function undo_last() {
    if (undo_list.length == 0) { return; }
    let last_action = undo_list[undo_list.length - 1];
    if (last_action['action'] == "moon") {
        document.getElementById(last_action['id']).innerHTML = last_action['prior_data'];
        collectedMoons.pop();
        index--;
    }
    undo_list.pop();
    if (undo_list.length == 0) { undo_btn.style.display = 'none'; }
}

initialize();
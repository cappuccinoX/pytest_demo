// update testcase name in results table, update by Michael on 2021.3.4
const case_name_td = document.getElementsByClassName('col-name');
for (let ele of case_name_td) {
    try {
        ele.innerText = ele.innerText.replace('tests/', '');
    } catch(e) {
        ele.innerText = "null";
    }
};
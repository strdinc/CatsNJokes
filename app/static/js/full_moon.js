const today = moment().format('YYYY-MM-DD');

const newMoonDays = ['2022-01-02', '2022-02-01', '2022-03-02', '2022-04-01', '2022-04-30', '2022-05-30', '2022-06-29', '2022-07-28', '2022-08-27', '2022-09-25', '2022-10-25', '2022-11-23', '2022-12-23'];
const fullMoonDays = ['2022-01-18', '2022-02-16', '2022-03-18', '2022-04-16', '2022-05-16', '2022-06-14', '2022-07-13', '2022-08-12', '2022-09-10', '2022-10-09', '2022-11-08', '2022-12-08'];

const nextFull = fullMoonDays.find(el => moment(el, 'YYYY-MM-DD').format('YYYY-MM-DD') >= today);
const nextNew = newMoonDays.find(el => moment(el, 'YYYY-MM-DD').format('YYYY-MM-DD') >= today);

const diff = moment(nextFull).diff(today, 'days');
const diffNew = moment(nextNew).diff(today, 'days');

const type = diff < diffNew ? "Full Moon" : 'New Moon';
const diffText = Math.min(diff, diffNew) > 1 ? `${Math.min(diff, diffNew)} days` : Math.min(diff, diffNew) === 1 ? `1 day` : '';

let className = '';
if (diff < diffNew) {
  className = diffNew > 0 ? `moon-full-${diff}` : 'moon-full';
} else {
  className = diffNew > 0 ? `moon-new-${diffNew}` : 'moon-new';

}
//className = 'moon-full-6'
const MOON = document.getElementById("moon");
const TYPE = document.getElementById("type");
const COUNT = document.getElementById("count");
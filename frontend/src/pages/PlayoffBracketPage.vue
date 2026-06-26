<template>
  <q-page class="playoff-page q-pa-lg">
    <div class="page-shell">
      <div class="row items-start justify-between q-col-gutter-md q-mb-lg">
        <div>
          <div class="text-h4 text-weight-bold">Сетка плейофф</div>
          <div class="text-body1 text-grey-7">
            Макет турнирной сетки для парных матчей с результатами по раундам.
          </div>
        </div>
        <q-btn outline color="primary" icon="arrow_back" label="На главную" to="/" no-caps />
      </div>
    </div>

    <div class="playoff-scroll">
      <div class="playoff-canvas">
        <svg class="playoff-lines" :viewBox="`0 0 ${canvasWidth} ${canvasHeight}`" aria-hidden="true">
          <path
            v-for="connector in connectors"
            :key="connector"
            :d="connector"
            fill="none"
            stroke="#d8dde3"
            stroke-width="2"
          />
        </svg>

        <div
          v-for="round in rounds"
          :key="round.id"
          class="playoff-round-title"
          :style="{ left: `${round.x}px` }"
        >
          {{ round.title }}
        </div>

        <q-card
          v-for="match in matches"
          :key="match.id"
          flat
          class="playoff-match-card"
          :class="{ 'playoff-match-card--final': match.round === 'final' }"
          :style="{ left: `${match.x}px`, top: `${match.y}px` }"
        >
          <div
            v-for="team in match.teams"
            :key="team.name"
            class="playoff-team-row"
            :class="{
              'playoff-team-row--winner': team.winner,
              'playoff-team-row--empty': team.score === null
            }"
          >
            <span class="playoff-team-name">{{ team.name }}</span>
            <span v-if="team.score !== null" class="playoff-team-score">{{ team.score }}</span>
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
interface PlayoffTeam {
  name: string;
  score: number | null;
  winner?: boolean;
}

interface PlayoffMatch {
  id: string;
  round: string;
  x: number;
  y: number;
  teams: [PlayoffTeam, PlayoffTeam];
}

const cardWidth = 280;
const cardHeight = 86;
const canvasWidth = 1400;
const canvasHeight = 880;

const rounds = [
  { id: 'r16', title: '1/8 финала', x: 38 },
  { id: 'r8', title: '1/4 финала', x: 398 },
  { id: 'r4', title: '1/2 финала', x: 758 },
  { id: 'final', title: 'Финал', x: 1118 }
];

const matches: PlayoffMatch[] = [
  {
    id: 'm1',
    round: 'r16',
    x: 0,
    y: 70,
    teams: [
      { name: 'Ярик / Денис Г', score: null, winner: true },
      { name: 'Иван / Сергей Б', score: null }
    ]
  },
  {
    id: 'm2',
    round: 'r16',
    x: 0,
    y: 166,
    teams: [
      { name: 'Иван / Сергей Б', score: 7, winner: true },
      { name: 'Дима М / Гена', score: 6 }
    ]
  },
  {
    id: 'm3',
    round: 'r16',
    x: 0,
    y: 282,
    teams: [
      { name: 'Коля / Рома Р', score: null, winner: true },
      { name: 'Дэн Ш / Маша', score: null }
    ]
  },
  {
    id: 'm4',
    round: 'r16',
    x: 0,
    y: 378,
    teams: [
      { name: 'Дэн Ш / Маша', score: null, winner: true },
      { name: 'Алена Н / Рома', score: null }
    ]
  },
  {
    id: 'm5',
    round: 'r16',
    x: 0,
    y: 494,
    teams: [
      { name: 'Алена Н / Рома', score: null },
      { name: 'Илья С / Лиза', score: null, winner: true }
    ]
  },
  {
    id: 'm6',
    round: 'r16',
    x: 0,
    y: 590,
    teams: [
      { name: 'Илья С / Лиза', score: null, winner: true },
      { name: 'Настя / Паша', score: null }
    ]
  },
  {
    id: 'm7',
    round: 'r16',
    x: 0,
    y: 706,
    teams: [
      { name: 'Настя / Паша', score: null, winner: true },
      { name: 'Костя / Миша', score: null }
    ]
  },
  {
    id: 'm8',
    round: 'r16',
    x: 0,
    y: 802,
    teams: [
      { name: 'Костя / Миша', score: null, winner: true },
      { name: 'Свободный слот', score: null }
    ]
  },
  {
    id: 'q1',
    round: 'r8',
    x: 360,
    y: 118,
    teams: [
      { name: 'Ярик / Денис Г', score: 7, winner: true },
      { name: 'Иван / Сергей Б', score: 6 }
    ]
  },
  {
    id: 'q2',
    round: 'r8',
    x: 360,
    y: 330,
    teams: [
      { name: 'Коля / Рома Р', score: 7, winner: true },
      { name: 'Дэн Ш / Маша', score: 6 }
    ]
  },
  {
    id: 'q3',
    round: 'r8',
    x: 360,
    y: 542,
    teams: [
      { name: 'Алена Н / Рома', score: 3 },
      { name: 'Илья С / Лиза', score: 7, winner: true }
    ]
  },
  {
    id: 'q4',
    round: 'r8',
    x: 360,
    y: 754,
    teams: [
      { name: 'Настя / Паша', score: 7, winner: true },
      { name: 'Костя / Миша', score: 5 }
    ]
  },
  {
    id: 's1',
    round: 'r4',
    x: 720,
    y: 224,
    teams: [
      { name: 'Ярик / Денис Г', score: 7, winner: true },
      { name: 'Коля / Рома Р', score: 3 }
    ]
  },
  {
    id: 's2',
    round: 'r4',
    x: 720,
    y: 648,
    teams: [
      { name: 'Илья С / Лиза', score: 3 },
      { name: 'Настя / Паша', score: 7, winner: true }
    ]
  },
  {
    id: 'f1',
    round: 'final',
    x: 1080,
    y: 436,
    teams: [
      { name: 'Ярик / Денис Г', score: 7, winner: true },
      { name: 'Настя / Паша', score: 6 }
    ]
  }
];

const links = [
  ['m1', 'q1'],
  ['m2', 'q1'],
  ['m3', 'q2'],
  ['m4', 'q2'],
  ['m5', 'q3'],
  ['m6', 'q3'],
  ['m7', 'q4'],
  ['m8', 'q4'],
  ['q1', 's1'],
  ['q2', 's1'],
  ['q3', 's2'],
  ['q4', 's2'],
  ['s1', 'f1'],
  ['s2', 'f1']
];

const matchById = new Map(matches.map((match) => [match.id, match]));

const connectors = links.map(([fromId, toId]) => {
  const from = matchById.get(fromId);
  const to = matchById.get(toId);

  if (!from || !to) {
    return '';
  }

  const startX = from.x + cardWidth;
  const startY = from.y + cardHeight / 2;
  const endX = to.x;
  const endY = to.y + cardHeight / 2;
  const middleX = startX + (endX - startX) / 2;

  return `M ${startX} ${startY} H ${middleX} V ${endY} H ${endX}`;
});
</script>

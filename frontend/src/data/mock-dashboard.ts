export type PlayerRow = {
  id: number;
  rank: number;
  initials: string;
  name: string;
  tier: string;
  rating: number;
  delta: number;
  accumulated: number;
  tournaments: number;
  matches: number;
  goals: number;
  wins: number;
  losses: number;
  winRate: string;
};

export const leagues = [
  'Все лиги',
  'Ярославская лига',
  'Москва Foos',
  'IT Companies League',
  'Лига бара Раскол'
];

export const players: PlayerRow[] = [
  {
    id: 4,
    rank: 1,
    initials: 'ЯД',
    name: 'Ярослав Двойных',
    tier: 'semi-pro',
    rating: 1656,
    delta: 15,
    accumulated: 7050,
    tournaments: 93,
    matches: 853,
    goals: 4647,
    wins: 492,
    losses: 236,
    winRate: '58%'
  },
  {
    id: 29,
    rank: 2,
    initials: 'ИН',
    name: 'Илья Нестеров',
    tier: 'semi-pro',
    rating: 1652,
    delta: -21,
    accumulated: 2370,
    tournaments: 41,
    matches: 284,
    goals: 1644,
    wins: 189,
    losses: 49,
    winRate: '67%'
  },
  {
    id: 47,
    rank: 3,
    initials: 'ИВ',
    name: 'Илья Вострилов',
    tier: 'semi-pro',
    rating: 1598,
    delta: -6,
    accumulated: 4500,
    tournaments: 65,
    matches: 453,
    goals: 2502,
    wins: 247,
    losses: 138,
    winRate: '55%'
  },
  {
    id: 12,
    rank: 4,
    initials: 'НШ',
    name: 'Николай Шергесов',
    tier: 'amateur',
    rating: 1447,
    delta: 36,
    accumulated: 4040,
    tournaments: 57,
    matches: 451,
    goals: 2355,
    wins: 236,
    losses: 139,
    winRate: '52%'
  }
];

export const tournaments = [
  {
    id: 'spring',
    title: 'Дипы в Расколе 2026',
    league: 'Ярославская лига',
    period: 'январь - июнь 2026',
    competitions: 18,
    players: 72,
    ratingMode: 'Лиговый коэффициент x1.2'
  },
  {
    id: 'it-cup',
    title: 'IT Cup Summer',
    league: 'IT Companies League',
    period: 'июнь - август 2026',
    competitions: 6,
    players: 44,
    ratingMode: 'Турнирный коэффициент x1.5'
  }
];

export const competitions = [
  {
    id: 'a-trip',
    title: 'A-trip 29.05.2026',
    date: '29.05.2026',
    tournament: 'Дипы в Расколе 2026',
    matches: 36,
    players: 18,
    winner: 'Илья Нестеров'
  },
  {
    id: 'friday',
    title: 'Пятница 22.05.26',
    date: '22.05.2026',
    tournament: 'Дипы в Расколе 2026',
    matches: 32,
    players: 16,
    winner: 'Ярослав Двойных'
  },
  {
    id: 'may15',
    title: '15 мая',
    date: '15.05.2026',
    tournament: 'Дипы в Расколе 2026',
    matches: 28,
    players: 14,
    winner: 'Павел Горбунов'
  }
];

export const matchRows = [
  {
    id: 1,
    round: 'Финал',
    teamA: 'Ярослав Двойных / Павел Горбунов',
    teamB: 'Илья Нестеров / Богдан Жаворонков',
    score: '7:5',
    globalDelta: '+15 / -15',
    leagueDelta: '+18 / -18',
    tournamentDelta: '+24 / -24'
  },
  {
    id: 2,
    round: 'Полуфинал',
    teamA: 'Илья Вострилов / Николай Шергесов',
    teamB: 'Ярослав Двойных / Павел Горбунов',
    score: '3:7',
    globalDelta: '-9 / +9',
    leagueDelta: '-12 / +12',
    tournamentDelta: '-16 / +16'
  },
  {
    id: 3,
    round: 'Группа A',
    teamA: 'Илья Нестеров / Артем Кузнецов',
    teamB: 'Денис Шахов / Николай Шергесов',
    score: '7:2',
    globalDelta: '+8 / -8',
    leagueDelta: '+11 / -11',
    tournamentDelta: '+14 / -14'
  }
];

export const timelineEvents = [
  {
    id: 1,
    date: '29.05.2026',
    title: 'Ярослав Двойных занял 3 место',
    subtitle: 'A-trip 29.05.2026',
    icon: 'emoji_events',
    color: 'amber-8'
  },
  {
    id: 2,
    date: '22.05.2026',
    title: 'Получил +61 рейтинга',
    subtitle: 'Лучший прирост недели в Ярославской лиге',
    icon: 'trending_up',
    color: 'positive'
  },
  {
    id: 3,
    date: '03.04.2026',
    title: 'Стал semi-pro',
    subtitle: 'Переход ранга после серии сильных матчей',
    icon: 'workspace_premium',
    color: 'indigo-7'
  },
  {
    id: 4,
    date: '27.03.2026',
    title: 'Выиграл соревнование',
    subtitle: 'Дип 27.03.2026',
    icon: 'military_tech',
    color: 'green-7'
  }
];

import { config } from '@vue/test-utils';

config.global.stubs = {
  QPage: {
    template: '<main><slot /></main>'
  },
  QBanner: {
    template: '<section><slot /></section>'
  },
  QBtn: {
    template: '<button><slot />{{ label }}</button>',
    props: ['label']
  },
  QCard: {
    template: '<section><slot /></section>'
  },
  QCardSection: {
    template: '<section><slot /></section>'
  },
  QChip: {
    template: '<span><slot /></span>'
  },
  QIcon: {
    template: '<i />'
  },
  QItem: {
    template: '<div><slot /></div>'
  },
  QItemLabel: {
    template: '<div><slot /></div>'
  },
  QItemSection: {
    template: '<div><slot /></div>'
  },
  QList: {
    template: '<div><slot /></div>'
  },
  QTable: {
    template: '<section><slot /></section>'
  },
  QTd: {
    template: '<td><slot /></td>'
  },
  QTimeline: {
    template: '<section><slot /></section>'
  },
  QTimelineEntry: {
    template: '<article>{{ title }}{{ subtitle }}<slot /></article>',
    props: ['title', 'subtitle']
  },
  RouterLink: {
    template: '<a><slot /></a>'
  }
};

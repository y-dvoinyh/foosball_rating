import { config } from '@vue/test-utils';

config.global.stubs = {
  QPage: {
    template: '<main><slot /></main>'
  },
  QBanner: {
    template: '<section><slot /></section>'
  }
};

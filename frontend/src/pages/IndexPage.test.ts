import { flushPromises, mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import IndexPage from './IndexPage.vue';
import { healthApiService } from 'src/services/api';

vi.mock('src/services/api', () => ({
  healthApiService: {
    getHealth: vi.fn()
  }
}));

const mockedGetHealth = vi.mocked(healthApiService.getHealth);

describe('IndexPage', () => {
  beforeEach(() => {
    mockedGetHealth.mockReset();
  });

  it('shows backend health status when request succeeds', async () => {
    mockedGetHealth.mockResolvedValue({
      status: 'ok',
      database: 'ok'
    });

    const wrapper = mount(IndexPage);
    await flushPromises();

    expect(mockedGetHealth).toHaveBeenCalled();
    expect(wrapper.text()).toContain('Публичная статистика кикера');
    expect(wrapper.text()).toContain('Backend health: ok, database: ok');
  });

  it('shows unavailable status when request fails', async () => {
    mockedGetHealth.mockRejectedValue(new Error('network error'));

    const wrapper = mount(IndexPage);
    await flushPromises();

    expect(wrapper.text()).toContain('Backend health: unavailable');
  });
});

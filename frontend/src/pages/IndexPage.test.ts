import { flushPromises, mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import IndexPage from './IndexPage.vue';
import { api } from 'boot/axios';

vi.mock('boot/axios', () => ({
  api: {
    get: vi.fn()
  }
}));

const mockedApiGet = vi.mocked(api.get);

describe('IndexPage', () => {
  beforeEach(() => {
    mockedApiGet.mockReset();
  });

  it('shows backend health status when request succeeds', async () => {
    mockedApiGet.mockResolvedValue({
      data: {
        status: 'ok',
        database: 'ok'
      }
    });

    const wrapper = mount(IndexPage);
    await flushPromises();

    expect(mockedApiGet).toHaveBeenCalledWith('/health');
    expect(wrapper.text()).toContain('Foosball Rating');
    expect(wrapper.text()).toContain('Backend health: ok, database: ok');
  });

  it('shows unavailable status when request fails', async () => {
    mockedApiGet.mockRejectedValue(new Error('network error'));

    const wrapper = mount(IndexPage);
    await flushPromises();

    expect(wrapper.text()).toContain('Backend health: unavailable');
  });
});

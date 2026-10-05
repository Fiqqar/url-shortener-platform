import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import UrlForm from '../src/components/UrlForm.vue'
import ShortUrlResult from '../src/components/ShortUrlResult.vue'

describe('UrlForm', () => {
  it('renders input and submit', () => {
    const w = mount(UrlForm, {
      props: { loading: false, modelValue: '', error: null },
    })
    expect(w.find('#url-input').exists()).toBe(true)
    expect(w.find('button[type="submit"]').exists()).toBe(true)
  })

  it('shows loading state and error', () => {
    const w = mount(UrlForm, {
      props: { loading: true, modelValue: 'https://x.com', error: 'Bad url' },
    })
    expect(w.find('button').attributes('disabled')).toBeDefined()
    expect(w.find('[role="alert"]').text()).toContain('Bad url')
  })

  it('emits submit', async () => {
    const w = mount(UrlForm, {
      props: { loading: false, modelValue: '', error: null },
    })
    await w.find('form').trigger('submit')
    expect(w.emitted('submit')).toBeTruthy()
  })
})

describe('ShortUrlResult', () => {
  it('displays short url and copy feedback', () => {
    const w = mount(ShortUrlResult, {
      props: {
        result: {
          code: 'abc123',
          short_url: 'http://localhost:8000/abc123',
          target_url: 'https://example.com/x',
        },
        copied: true,
      },
    })
    expect(w.text()).toContain('http://localhost:8000/abc123')
    expect(w.text()).toContain('Copied!')
  })
})

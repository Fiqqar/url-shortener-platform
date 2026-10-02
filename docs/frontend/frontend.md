# Frontend Implementation

## 39. Frontend Implementation

The Vue frontend should provide a simple user interface for the URL shortener.

Initial functionality:

- URL input
- client-side validation
- submit action
- generated short URL display
- copy-to-clipboard action
- basic error display
- analytics lookup
- loading states

The frontend should prioritize usability and clarity over visual complexity.

---

## 40. Frontend Structure

Suggested structure:

    frontend/src/
    ├── components/
    │   ├── UrlForm.vue
    │   ├── ShortUrlResult.vue
    │   └── AnalyticsCard.vue
    │
    ├── views/
    │   ├── HomeView.vue
    │   └── AnalyticsView.vue
    │
    ├── services/
    │   └── api.ts
    │
    ├── composables/
    │   └── useUrlShortener.ts
    │
    ├── types/
    │   └── api.ts
    │
    ├── router/
    │   └── index.ts
    │
    ├── App.vue
    └── main.ts

The exact component structure may evolve.

Avoid creating a component for every trivial HTML element.

---

## 41. Frontend API Layer

All backend API communication should be centralized.

Do not scatter raw `fetch()` calls throughout Vue components.

Preferred pattern:

    Component
        |
        v
    Composable
        |
        v
    API Service
        |
        v
    FastAPI

The API service should handle:

- request construction
- base URL configuration
- JSON serialization
- response parsing
- API error handling

---

## 42. Frontend Types

Use TypeScript interfaces or types for API responses.

Example:

    interface CreateUrlRequest {
      url: string
    }

    interface CreateUrlResponse {
      code: string
      short_url: string
      target_url: string
    }

Types should reflect the backend API contract.

Avoid using `any` for API data unless there is a documented reason.

---

## 43. Frontend State

Keep state close to the component or composable that owns it.

Typical state:

- input URL
- loading state
- generated result
- error message
- analytics data

Do not introduce a global state management library unless application complexity requires it.

For the initial application, Vue composables and component state should be sufficient.

---

## 44. Frontend Validation

Client-side validation should provide immediate feedback.

At minimum:

- reject empty input
- validate URL syntax
- prevent obviously unsupported protocols
- show useful validation messages

Client-side validation is for user experience.

It must never replace backend validation.

---

## 45. Frontend Error Handling

The frontend should distinguish between:

- validation errors
- API client errors
- not-found errors
- server errors
- network failures

Error messages should be understandable to users.

Do not display raw backend stack traces or internal exception messages.

---

## 46. Copy-to-Clipboard

The generated short URL should provide a convenient copy action.

The implementation should:

- use the browser Clipboard API where supported
- provide feedback after successful copying
- handle unsupported or failed clipboard operations gracefully

Do not make clipboard functionality a dependency for core URL creation.

---

## 47. Frontend Testing

Use Vitest and Vue Test Utils.

Tests should cover:

### Components

- URL form renders
- invalid input is rejected
- submit action works
- loading state is displayed
- result is displayed
- errors are displayed
- copy action behaves correctly

### API service

- successful request parsing
- API error handling
- network failure behavior

### Composables

- state transitions
- loading state
- successful creation
- error handling

Avoid relying on real backend services in unit tests.

Mock API requests where appropriate.

---


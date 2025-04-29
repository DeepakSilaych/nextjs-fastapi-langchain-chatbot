# Frontend – AI Chat Application
+ [🔗 Root README](../README.md) | [🔧 Backend README](../backend/README.md)
+ [![Modular](https://img.shields.io/badge/Modular-Frontend-blue)](#architecture--modularity)

 This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Architecture & Modularity
A visual map of frontend modules and dependencies:

![Frontend Architecture](../docs/frontend_architecture.png)

Modules & Stats:
- **Components**: 12 React components (ChatWindow, FileUpload, InputBox, MessageBubble, SettingsDialog, Sidebar, UI/Dialog, ...)
- **Hooks**: 2 custom hooks (`useChat`, `useUpload`)
- **Pages**: 5 routes (`/`, `/chat/[id]`, `/upload`, `/history`, 404)
- **Utilities**: API client, helper functions (`utils/api.ts`)
- **Styles**: global (globals.css) + Tailwind

## Extending the Frontend
Learn to swap or add modules:
1. **Adding a new Component**
   - Create `components/YourComponent.tsx`
   - Import and use in a page or layout
2. **Integrating a UI Library**
   - Install with `npm install <library>`
   - Wrap app in provider via `app/layout.tsx`
3. **Adding a New Page/Route**
   - Create `app/yourRoute/page.tsx`
   - Update navigation in `Sidebar.tsx`

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

---

Dive deeper:
- 📖 [Root README](../README.md)
- 📖 [Backend README](../backend/README.md)

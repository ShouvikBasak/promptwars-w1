# Implementation Plan: Attractive StadiumFlow GUI

Transform the basic `index.html` into a premium, modern attendee dashboard called the **"StadiumFlow Hub"**.

## User Review Required

> [!IMPORTANT]
> **Single Dashboard**: I will unify the experience into a single, highly-polished page that handles attendee recommendations. I will keep the `ops.html` separate but give it a matching "Dark Mode Pro" aesthetic.

## Proposed Changes

### UI/UX Redesign

#### [MODIFY] [index.html](file:///c:/Users/sbasak2/OneDrive%20-%20DXC%20Production/myRepos/promptwars-w1/index.html)
- **Concept**: "Stadium Night Mode" – A glassmorphic interface with vibrant gradients and blur effects.
- **Features**:
  - Animated hero section with stadium floor-plan aesthetic.
  - Interactive "Zone Selector" with custom designed dropdowns/buttons.
  - "AI Insights" cards for recommendations with progress/confidence indicators.
  - Smooth scale and fade animations using CSS transitions.
  - Lucide icons for POI types (restroom, food, exit).

#### [MODIFY] [ops.html](file:///c:/Users/sbasak2/OneDrive%20-%20DXC%20Production/myRepos/promptwars-w1/ops.html)
- **Concept**: "Command Center" – A clean, professional dark-theme version of the attendee UI focused on speed and data density.
- **Features**:
  - Quick-action grid for staff overrides.
  - Modernized status tables with status badges.

## Verification Plan

### Automated Tests
- I'll use the browser tool to verify the visual layout and ensure the buttons correctly trigger the AI API calls.

### Manual Verification
- You will see the new UI at your Cloud Run URL. It will feature:
  - Glass effect panels.
  - Vibrant "Stadium Glow" backgrounds.
  - Modern "Outfit" typography.

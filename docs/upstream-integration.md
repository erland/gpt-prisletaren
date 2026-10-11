# Integrering av GPT Byggarens canonical distributionsmotor

## Importerat
- Kanoniska `build_distributions.py`, `validate_distributions.py` och `lib/project_model.py`.
- `PyYAML` som byggberoende.
- Fail-closed tester som hindrar påstådd runtimeparitet utan uppfyllda förutsättningar.

## Kvarstående blockerare
1. Skapa fullständigt `gpt-project.yaml` enligt upstream-schema, inklusive `build_system.runtime_targets`, `runtime`, projekt-/förmåge-/artefakt-/toolkontrakt och kunskapsstruktur.
2. Tillför de runtime-specifika mallar och resurser som upstream-bygget kräver.
3. Anpassa och validera ChatGPT Chat och OpenAI Plugin som egna, jämförbara men inte identiska runtimeprojektioner.
4. Kör upstream bygg- OCH distributionsvalidering i CI mot faktiska producerade paket; jämför med Prisletarens befintliga beteende.
5. Flytta releaseworkflow från `tools/build.py` först efter godkänd verifiering, och lägg till ett release-readiness-gate.

## Releasepolicy
Det nuvarande releaseworkflowet ska inte triggas genom tagg förrän blockerarna ovan har åtgärdats. Inga befintliga Chat/Plugin-instruktioner eller runtimekontrakt ändras av denna import.

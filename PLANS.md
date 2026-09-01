# ExecPlan Template

복수 파일 수정, 환경 구축, 외부 모델 통합, 3개 이상의 검증 단계가 필요한 작업에 사용한다. 계획은 `state/CURRENT_TUTORIAL.md`에 기록하고 실행 중 갱신한다.

```markdown
# Txx — <title>

## Objective
한 문장으로 완료 상태를 정의한다.

## Current facts
- 현재 OS/architecture:
- 활성 환경:
- 필요한 모델 commit:
- 이미 존재하는 코드:

## Constraints
- 수정 금지 경로:
- 사용 가능한 GPU/GUI:
- 안전 제한:

## Work items
- [ ] Preflight
- [ ] Minimal implementation
- [ ] Tests
- [ ] Interactive or offscreen visualization
- [ ] Metrics and report
- [ ] State update

## Verification commands
```bash
<commands>
```

## Expected artifacts
- `...`

## Decisions and deviations
- 계획과 달라진 점과 이유를 실행 중 기록한다.
```

계획은 작업을 대신하지 않는다. 가능한 한 같은 세션에서 구현과 검증까지 완료한다.

# cron-setup.md -- Scheduling `knowledge_updater.py`

This document explains how to run `tools/knowledge_updater.py` on a regular schedule so that
`SECOND-KNOWLEDGE-BRAIN.md` stays current with the latest humanitarian logistics research,
situation reports, and disaster alerts.

## Recommended Schedule

| Source | Frequency | Rationale |
|--------|-----------|-----------|
| ReliefWeb, HDX, ALNAP, OCHA analysis, Emerald JHL, ArXiv, Sphere | Weekly (Sundays 00:00 UTC) | Sitreps and research publications update weekly; avoids rate limits |
| GDACS alerts | Daily (00:00 UTC) | Active disasters and weather alerts change rapidly |

---

## Linux / macOS (cron)

### 1. Make the script executable (optional)
```bash
chmod +x /path/to/repo/tools/knowledge_updater.py
```

### 2. Weekly run (all sources except daily GDACS)
```cron
# Weekly knowledge refresh, Sundays at 00:00 UTC
0 0 * * 0 cd /path/to/repo && /usr/bin/python3 tools/knowledge_updater.py >> tools/updater.log 2>&1
```

### 3. Daily GDACS run
```cron
# GDACS active disaster alerts, daily at 00:00 UTC
0 0 * * * cd /path/to/repo && /usr/bin/python3 tools/knowledge_updater.py --source gdacs >> tools/updater.log 2>&1
```

### 4. Verify the cron job is registered
```bash
crontab -l
```

---

## Windows (Task Scheduler)

### Weekly run (all sources)
1. Open **Task Scheduler** (`taskschd.msc`).
2. Click **Create Basic Task...**.
3. Name: `Skill242 Knowledge Updater - Weekly`
4. Trigger: **Weekly** ? every **Sunday** at **00:00:00**.
5. Action: **Start a program**
6. Program/script: `python`
7. Add arguments: `"C:\path\to\repo\tools\knowledge_updater.py"`
8. Start in: `C:\path\to\repo`
9. Finish, then open the task properties and check:
   - **Run whether user is logged on or not** (optional)
   - **Run with highest privileges** (only if the script needs admin access)
   - **If the task fails, restart every:** 10 minutes, up to 3 attempts

### Daily GDACS run
Repeat the steps above with:
- Name: `Skill242 GDACS Daily`
- Trigger: **Daily** at **00:00:00**
- Arguments: `"C:\path\to\repo\tools\knowledge_updater.py" --source gdacs`

### Verify
Open `tools/updater.log` after the scheduled time to confirm the run completed:
```
Entries appended to SECOND-KNOWLEDGE-BRAIN.md: N
```

---

## Docker / Container Deployment

If running in a container, use the host cron or an orchestrator such as Kubernetes CronJob.

### Kubernetes CronJob example (weekly)
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: skill242-knowledge-updater
spec:
  schedule: "0 0 * * 0"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: updater
            image: python:3.11-slim
            command:
              - python
              - /repo/tools/knowledge_updater.py
            volumeMounts:
            - name: repo
              mountPath: /repo
          restartPolicy: OnFailure
          volumes:
          - name: repo
            hostPath:
              path: /path/to/repo
```

---

## Dry-run testing before scheduling

Always test the command manually before scheduling it:

```bash
cd /path/to/repo
python tools/knowledge_updater.py --dry-run
```

This fetches and scores entries without writing to `SECOND-KNOWLEDGE-BRAIN.md`, so you
can verify sources and rate limits before enabling the live schedule.

---

## Monitoring and alerts

- Check `tools/updater.log` for each run summary.
- If a source repeatedly fails (e.g., rate limited or site structure changed), the script
  logs a warning and continues; the failure does not block other sources.
- Deduplication is handled by `tools/crawled_ids.json`. Delete this file only if you want
to re-ingest previously seen URLs.

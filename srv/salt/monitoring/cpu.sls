check_cpu:
  cpu.status:
    - url: http://test.internal/{{ grains.id }}/disk.status/
    - thresholds:
      - critical:
          maximum: 90
      - warning:
          maximum: 70
      - ok:
          result: True

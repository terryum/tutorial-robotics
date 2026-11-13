<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/setup/latest-robotics.md" lang="ko">한국어</a> | <a href="latest-robotics.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Latest robotics installation

Mac is a development/client host; Ubuntu executes the GPU workloads.

[Installation, verification, release watch and pending acceptance](https://github.com/terryum/tutorial-robotics/blob/main/setup/LATEST_ROBOTICS_UPDATE.md)

```bash
pal stack plan --profile pi05 --json
pal stack discover --profile pi05 --json
```

Prepared profiles remain GPU-unverified. GR00T 2 code is announced for December;
installing N1.7 does not validate GR00T 2.

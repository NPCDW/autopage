# 自动化测试项目

> 需要使用家宽才能过 cf 的验证

请先配置 `data/config.json` 文件

cf 通过测试
```shell
python3 -m src.solver.cf_solver
```
ns签到
```shell
python3 -m src.nodeseek_checkin
```
akile签到
```shell
python3 -m src.akile_checkin
```
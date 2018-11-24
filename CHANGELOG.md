# Change Log

## [v1.0.0-beta.2](https://github.com/kabirbaidhya/boss/tree/v1.0.0-beta.2) (2018-11-24)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-beta.1...v1.0.0-beta.2)

**Improvements:**

- Improvements and tests on the slack url config [\#143](https://github.com/kabirbaidhya/boss/pull/143) [[test](https://github.com/kabirbaidhya/boss/labels/test)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Support full slack endpoint url in the config [\#141](https://github.com/kabirbaidhya/boss/pull/141) [[notification](https://github.com/kabirbaidhya/boss/labels/notification)] ([squgeim](https://github.com/squgeim))

## [v1.0.0-beta.1](https://github.com/kabirbaidhya/boss/tree/v1.0.0-beta.1) (2018-10-31)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.20...v1.0.0-beta.1)

**Improvements:**

- Make build script optional supporting node projects w/o build script [\#138](https://github.com/kabirbaidhya/boss/pull/138) [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.20](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.20) (2018-10-30)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.19...v1.0.0-alpha.20)

**Fixed bugs:**

- Fix build directory removal issue due to fs.glob\(\) having ANSI color codes in it [\#134](https://github.com/kabirbaidhya/boss/pull/134) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Ability to use vault for credentials for deployment [\#131](https://github.com/kabirbaidhya/boss/issues/131) [[config](https://github.com/kabirbaidhya/boss/labels/config)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)]

**Improvements:**

- Fix CVE-2018-18074 vulnerablility due to requests [\#137](https://github.com/kabirbaidhya/boss/pull/137) [[security](https://github.com/kabirbaidhya/boss/labels/security)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Upgrade fabric and paramiko version [\#136](https://github.com/kabirbaidhya/boss/pull/136) ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.19](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.19) (2018-10-11)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.18...v1.0.0-alpha.19)

**Implemented enhancements:**

- Make install script optional for node and web deployments [\#133](https://github.com/kabirbaidhya/boss/pull/133) [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Fixed bugs:**

- Deployment fails if public\_url is not provided for each stage [\#111](https://github.com/kabirbaidhya/boss/issues/111) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)]

**Improvements:**

- Support vault integration for injection of secrets in boss.yml and local execution context [\#132](https://github.com/kabirbaidhya/boss/pull/132) [[config](https://github.com/kabirbaidhya/boss/labels/config)] [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.18](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.18) (2018-10-09)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.17...v1.0.0-alpha.18)

**Improvements:**

- Add deployment hook scripts pre\_deploy and post\_deploy  [\#129](https://github.com/kabirbaidhya/boss/pull/129) [[config](https://github.com/kabirbaidhya/boss/labels/config)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add install hook scripts pre\_install and post\_install [\#128](https://github.com/kabirbaidhya/boss/pull/128) [[config](https://github.com/kabirbaidhya/boss/labels/config)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add build hook scripts pre\_build and post\_build [\#127](https://github.com/kabirbaidhya/boss/pull/127) [[config](https://github.com/kabirbaidhya/boss/labels/config)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Fix CVE-2018-7750 security vulnerability [\#126](https://github.com/kabirbaidhya/boss/pull/126) ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.17](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.17) (2018-02-11)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.16...v1.0.0-alpha.17)

**Implemented enhancements:**

- Better wording for script running notification message [\#116](https://github.com/kabirbaidhya/boss/pull/116) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[notification](https://github.com/kabirbaidhya/boss/labels/notification)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Support flexible notification messages [\#114](https://github.com/kabirbaidhya/boss/pull/114) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[notification](https://github.com/kabirbaidhya/boss/labels/notification)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.16](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.16) (2018-02-06)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-experimental.1...v1.0.0-alpha.16)

## [v1.0.0-experimental.1](https://github.com/kabirbaidhya/boss/tree/v1.0.0-experimental.1) (2018-01-13)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.15...v1.0.0-experimental.1)

**Implemented enhancements:**

- Resolve remote cwd and normalize remote paths correctly [\#104](https://github.com/kabirbaidhya/boss/pull/104) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[experimental](https://github.com/kabirbaidhya/boss/labels/experimental)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Fixed bugs:**

- Ignore notification failure, and proceed even if sending notification fails  [\#108](https://github.com/kabirbaidhya/boss/pull/108) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Improvements:**

- Support running a list of commands with ssh.run\(\) function [\#109](https://github.com/kabirbaidhya/boss/pull/109) [[api](https://github.com/kabirbaidhya/boss/labels/api)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Refactor buildman and node deployment [\#107](https://github.com/kabirbaidhya/boss/pull/107) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] [[experimental](https://github.com/kabirbaidhya/boss/labels/experimental)] [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Normalize remote path while invoking ssh.upload\_dir\(\) [\#106](https://github.com/kabirbaidhya/boss/pull/106) [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Introduce ssh.upload\_dir\(\) to upload a local directory to the remote host [\#105](https://github.com/kabirbaidhya/boss/pull/105) [[api](https://github.com/kabirbaidhya/boss/labels/api)] [[experimental](https://github.com/kabirbaidhya/boss/labels/experimental)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Check if remote is up to date on deployment [\#103](https://github.com/kabirbaidhya/boss/pull/103) [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Rewrite basic ssh operations using the new ssh module w/o relying on fabric [\#101](https://github.com/kabirbaidhya/boss/pull/101) [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] [[test](https://github.com/kabirbaidhya/boss/labels/test)] [[wip](https://github.com/kabirbaidhya/boss/labels/wip)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.15](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.15) (2017-12-27)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.14...v1.0.0-alpha.15)

**Fixed bugs:**

- Fix weird `\<pre\>` tag hipchat notifcation issue  [\#102](https://github.com/kabirbaidhya/boss/pull/102) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.14](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.14) (2017-12-25)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.13...v1.0.0-alpha.14)

**Closed issues:**

- Generic task notifications about configured scripts [\#91](https://github.com/kabirbaidhya/boss/issues/91) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[notification](https://github.com/kabirbaidhya/boss/labels/notification)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)]

**Improvements:**

- Support custom scripts notifications [\#100](https://github.com/kabirbaidhya/boss/pull/100) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[notification](https://github.com/kabirbaidhya/boss/labels/notification)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add basic SSH and SFTP functions directly over paramiko [\#98](https://github.com/kabirbaidhya/boss/pull/98) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Refactor utils [\#96](https://github.com/kabirbaidhya/boss/pull/96) [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Refactor config constants and move them to separate constant files. [\#95](https://github.com/kabirbaidhya/boss/pull/95) [[internals](https://github.com/kabirbaidhya/boss/labels/internals)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Change config default values for user and base\_dir [\#94](https://github.com/kabirbaidhya/boss/pull/94) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] [[config](https://github.com/kabirbaidhya/boss/labels/config)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.13](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.13) (2017-12-23)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.12...v1.0.0-alpha.13)

**Implemented enhancements:**

- Add core utils for compression and hashing [\#93](https://github.com/kabirbaidhya/boss/pull/93) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Remote environment variables injection [\#89](https://github.com/kabirbaidhya/boss/issues/89) [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[interesting](https://github.com/kabirbaidhya/boss/labels/interesting)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)]

**Improvements:**

- Remote env injection [\#92](https://github.com/kabirbaidhya/boss/pull/92) [[deployment](https://github.com/kabirbaidhya/boss/labels/deployment)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[remote execution](https://github.com/kabirbaidhya/boss/labels/remote%20execution)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.12](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.12) (2017-11-24)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.11...v1.0.0-alpha.12)

**Implemented enhancements:**

- Display CI link on notification messages if running on CI [\#86](https://github.com/kabirbaidhya/boss/pull/86) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Display CI build link on notification messages if running on CI [\#85](https://github.com/kabirbaidhya/boss/issues/85) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)]

## [v1.0.0-alpha.11](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.11) (2017-11-21)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.10...v1.0.0-alpha.11)

**Implemented enhancements:**

- Use separate colors for notification messages for CI and manual deployments [\#84](https://github.com/kabirbaidhya/boss/pull/84) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.10](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.10) (2017-11-21)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.9...v1.0.0-alpha.10)

**Implemented enhancements:**

- Use git tree url for commit and branch links in the notification message [\#83](https://github.com/kabirbaidhya/boss/pull/83) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Display commit hash on slack and hipchat deployment notifications [\#82](https://github.com/kabirbaidhya/boss/pull/82) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Refactor boss.config and add tests to verify things work correctly [\#80](https://github.com/kabirbaidhya/boss/pull/80) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[refactor](https://github.com/kabirbaidhya/boss/labels/refactor)] [[test](https://github.com/kabirbaidhya/boss/labels/test)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.9](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.9) (2017-11-17)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.8...v1.0.0-alpha.9)

**Fixed bugs:**

- Fix deployment finish notification message issue [\#79](https://github.com/kabirbaidhya/boss/pull/79) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.8](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.8) (2017-11-15)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.7...v1.0.0-alpha.8)

**Implemented enhancements:**

- Support for '--interactive' option for 'boss init' [\#75](https://github.com/kabirbaidhya/boss/pull/75) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([srishanbhattarai](https://github.com/srishanbhattarai))

**Fixed bugs:**

- Fix the build directory not found issue on deployment [\#77](https://github.com/kabirbaidhya/boss/pull/77) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Fix the misleading resolving env file message [\#76](https://github.com/kabirbaidhya/boss/pull/76) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.7](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.7) (2017-10-30)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.6...v1.0.0-alpha.7)

**Implemented enhancements:**

- Simplify slack deployment message format [\#71](https://github.com/kabirbaidhya/boss/pull/71) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([mesaugat](https://github.com/mesaugat))
- Display .env filename being resolved while running tasks [\#70](https://github.com/kabirbaidhya/boss/pull/70) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add `t` for automating manual tasks. [\#66](https://github.com/kabirbaidhya/boss/pull/66) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add `init` command in the boss CLI [\#62](https://github.com/kabirbaidhya/boss/pull/62) [[cli](https://github.com/kabirbaidhya/boss/labels/cli)] [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Simplify deploying output with a shorter message [\#57](https://github.com/kabirbaidhya/boss/pull/57) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Use default values to simplify common boss configuration  [\#56](https://github.com/kabirbaidhya/boss/pull/56) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Write unit tests and configure Travis CI [\#48](https://github.com/kabirbaidhya/boss/issues/48) [[good first issue](https://github.com/kabirbaidhya/boss/labels/good%20first%20issue)] [[help wanted](https://github.com/kabirbaidhya/boss/labels/help%20wanted)]
- Need a new cli command `boss init` [\#35](https://github.com/kabirbaidhya/boss/issues/35) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] [[hacktoberfest](https://github.com/kabirbaidhya/boss/labels/hacktoberfest)]
- Ability to use the Boss CLI interface [\#20](https://github.com/kabirbaidhya/boss/issues/20)

**Improvements:**

- Consistent wording for README text [\#73](https://github.com/kabirbaidhya/boss/pull/73) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([srishanbhattarai](https://github.com/srishanbhattarai))
- Website Design Overhaul [\#69](https://github.com/kabirbaidhya/boss/pull/69) [[design](https://github.com/kabirbaidhya/boss/labels/design)] [[ux](https://github.com/kabirbaidhya/boss/labels/ux)] ([sshikhrakar](https://github.com/sshikhrakar))
- Boss logo update to version 2.0 and readme alignment updates [\#68](https://github.com/kabirbaidhya/boss/pull/68) [[design](https://github.com/kabirbaidhya/boss/labels/design)] [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] [[ux](https://github.com/kabirbaidhya/boss/labels/ux)] ([sshikhrakar](https://github.com/sshikhrakar))
- Fix general typos [\#67](https://github.com/kabirbaidhya/boss/pull/67) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([enzosk8](https://github.com/enzosk8))
- Configure Travis CI and make CLI tests pass [\#63](https://github.com/kabirbaidhya/boss/pull/63) [[cli](https://github.com/kabirbaidhya/boss/labels/cli)] [[test](https://github.com/kabirbaidhya/boss/labels/test)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add badges on the README [\#58](https://github.com/kabirbaidhya/boss/pull/58) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.6](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.6) (2017-10-16)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.5...v1.0.0-alpha.6)

**Closed issues:**

- Remove deprecated features [\#26](https://github.com/kabirbaidhya/boss/issues/26) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)]
- Independence from the tools like npm, systemctl [\#17](https://github.com/kabirbaidhya/boss/issues/17)

**Improvements:**

- Change default branch to `master` from `dev` [\#55](https://github.com/kabirbaidhya/boss/pull/55) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Ability to resolve stage-specific `.env` file based on the deployment/task stage [\#54](https://github.com/kabirbaidhya/boss/pull/54) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Remote deprecated features [\#52](https://github.com/kabirbaidhya/boss/pull/52) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.5](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.5) (2017-10-12)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.4...v1.0.0-alpha.5)

**Improvements:**

- Add `verbose\_logging` option to display paramiko/ssh logs [\#47](https://github.com/kabirbaidhya/boss/pull/47) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
-  Add ssh\_forward\_agent config option [\#46](https://github.com/kabirbaidhya/boss/pull/46) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.4](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.4) (2017-10-12)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.3...v1.0.0-alpha.4)

**Improvements:**

- Rename preset wording frontend to web [\#45](https://github.com/kabirbaidhya/boss/pull/45) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add support for nodejs project deployment [\#44](https://github.com/kabirbaidhya/boss/pull/44) [[breaking-change](https://github.com/kabirbaidhya/boss/labels/breaking-change)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add logo in the README [\#41](https://github.com/kabirbaidhya/boss/pull/41) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.3](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.3) (2017-09-08)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.2...v1.0.0-alpha.3)

**Fixed bugs:**

- Fix SSH user not being overridden for each stage for frontend deployment [\#43](https://github.com/kabirbaidhya/boss/issues/43) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)]

## [v1.0.0-alpha.2](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.2) (2017-09-05)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v1.0.0-alpha.1...v1.0.0-alpha.2)

**Improvements:**

- Support stage-specific deployment configuration [\#42](https://github.com/kabirbaidhya/boss/pull/42) ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v1.0.0-alpha.1](https://github.com/kabirbaidhya/boss/tree/v1.0.0-alpha.1) (2017-08-24)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v0.3.0...v1.0.0-alpha.1)

**Closed issues:**

- Add configuration documentation [\#24](https://github.com/kabirbaidhya/boss/issues/24) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)]
- Zero-downtime rollback [\#18](https://github.com/kabirbaidhya/boss/issues/18)
- Support for zero-downtime frontend deployment [\#14](https://github.com/kabirbaidhya/boss/issues/14)
- Add support for deployment presets [\#13](https://github.com/kabirbaidhya/boss/issues/13)

**Improvements:**

- Add instructions for frontend deployment in the README [\#40](https://github.com/kabirbaidhya/boss/pull/40) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add `setup` task to setup remote for deployment [\#39](https://github.com/kabirbaidhya/boss/pull/39) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Fix configuration documentation typos [\#38](https://github.com/kabirbaidhya/boss/pull/38) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([sanjeevkpandit](https://github.com/sanjeevkpandit))
- Add support for Frontend Deployment [\#33](https://github.com/kabirbaidhya/boss/pull/33) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add documentation for remote source deployment [\#32](https://github.com/kabirbaidhya/boss/pull/32) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Support deployment preset and change the default deployment to remote source deployment preset [\#31](https://github.com/kabirbaidhya/boss/pull/31) [[deprecation](https://github.com/kabirbaidhya/boss/labels/deprecation)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))

## [v0.3.0](https://github.com/kabirbaidhya/boss/tree/v0.3.0) (2017-08-15)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v0.2.2...v0.3.0)

**Implemented enhancements:**

- Better informative info messages for deployment and remote tasks [\#30](https://github.com/kabirbaidhya/boss/pull/30) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Make use of custom scripts in deployment and other tasks [\#29](https://github.com/kabirbaidhya/boss/pull/29) [[deprecation](https://github.com/kabirbaidhya/boss/labels/deprecation)] [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Ability to inject environment variables in boss.yml  [\#21](https://github.com/kabirbaidhya/boss/issues/21)
- Add support for custom scripts [\#16](https://github.com/kabirbaidhya/boss/issues/16)

**Improvements:**

- Add Code of Conduct [\#28](https://github.com/kabirbaidhya/boss/pull/28) [[documentation](https://github.com/kabirbaidhya/boss/labels/documentation)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Interpolate environment variables in boss.yml [\#27](https://github.com/kabirbaidhya/boss/pull/27) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Support custom scripts similar to npm scripts [\#25](https://github.com/kabirbaidhya/boss/pull/25) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Update boss.yml.example [\#23](https://github.com/kabirbaidhya/boss/pull/23) ([sanjeevkpandit](https://github.com/sanjeevkpandit))

## [v0.2.2](https://github.com/kabirbaidhya/boss/tree/v0.2.2) (2017-08-10)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v0.2.1...v0.2.2)

**Fixed bugs:**

- Error installing boss-cli==0.2.1 due to README.md error [\#22](https://github.com/kabirbaidhya/boss/issues/22) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)]

## [v0.2.1](https://github.com/kabirbaidhya/boss/tree/v0.2.1) (2017-08-09)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v0.2.0...v0.2.1)

**Implemented enhancements:**

- Allow setting private key \(pem\) file via boss.yml [\#11](https://github.com/kabirbaidhya/boss/pull/11) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([kabirbaidhya](https://github.com/kabirbaidhya))

**Closed issues:**

- Support adding SSH pemfile for each stage in the boss.yml file [\#10](https://github.com/kabirbaidhya/boss/issues/10)

## [v0.2.0](https://github.com/kabirbaidhya/boss/tree/v0.2.0) (2017-07-20)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/v0.1.1...v0.2.0)

**Fixed bugs:**

- Unable to deploy due to git checkout error [\#8](https://github.com/kabirbaidhya/boss/issues/8) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)]

**Closed issues:**

- Does not support OS without systemctl [\#1](https://github.com/kabirbaidhya/boss/issues/1)

**Improvements:**

- One step closer to systemctl independence [\#9](https://github.com/kabirbaidhya/boss/pull/9) [[deprecation](https://github.com/kabirbaidhya/boss/labels/deprecation)] ([kabirbaidhya](https://github.com/kabirbaidhya))
- Add boss icon for bot [\#7](https://github.com/kabirbaidhya/boss/pull/7) ([sanjeevkpandit](https://github.com/sanjeevkpandit))

## [v0.1.1](https://github.com/kabirbaidhya/boss/tree/v0.1.1) (2017-05-31)
[Full Changelog](https://github.com/kabirbaidhya/boss/compare/0.0.1...v0.1.1)

**Implemented enhancements:**

- Ability to set port from boss.yml file [\#2](https://github.com/kabirbaidhya/boss/issues/2) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)]
- Replace curl with requests [\#6](https://github.com/kabirbaidhya/boss/pull/6) [[enhancement](https://github.com/kabirbaidhya/boss/labels/enhancement)] ([squgeim](https://github.com/squgeim))

**Fixed bugs:**

- Ability to override user for each stage [\#3](https://github.com/kabirbaidhya/boss/issues/3) [[bug](https://github.com/kabirbaidhya/boss/labels/bug)]

**Improvements:**

- Add Hipchat notification support [\#5](https://github.com/kabirbaidhya/boss/pull/5) [[feature](https://github.com/kabirbaidhya/boss/labels/feature)] ([squgeim](https://github.com/squgeim))

## [0.0.1](https://github.com/kabirbaidhya/boss/tree/0.0.1) (2017-04-12)


\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
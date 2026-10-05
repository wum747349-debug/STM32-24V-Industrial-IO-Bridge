# Hardware Revision History

## Rev.C — Current Hardware

Status:

- Third hardware iteration
- Hardware fabricated and assembled
- Basic functional bring-up and debugging completed
- Currently in practical use

Major changes from the previous revision:

- Added photoelectric-sensor field power and NO / NC signal interfaces
- Added onboard USB-C and CH340C USB-UART communication
- Added ISO7721 digital isolation between USB-side and machine-side domains
- Replaced the external STM32 minimum-system module with an onboard STM32 minimum system
- Added or improved 24 V reverse-polarity, input, and onboard power-conversion protection boundaries

Validation boundary:

Rev.C has completed practical functional debugging and is in use, but the repository does not claim complete quantified electrical characterization, EMC/surge qualification, isolation-withstand certification, or full formal system acceptance.

## Earlier Iterations

Rev.A and Rev.B existed as previous hardware iterations. Their detailed circuit changes, dates, and test histories are not reconstructed in this repository.

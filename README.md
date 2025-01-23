# **Content Roulette bot for FFXIV**
Simple discord bot that randomly rolls an 8 man FFXIV encounter and randomly assign jobs to players
## How to use
### **`!play`**
Bot will respond with the prompt and react with :pregnant_man:

Waits for 8 separate users (not including bot) to react :pregnant_man: 
![When !play is called](https://cdn.discordapp.com/attachments/333422790612877323/1331691275333800037/image.png?ex=67933265&is=6791e0e5&hm=6ef52f43c941b4b84fbdc2d50db9799a3512c25226d68e0460b758cfa7cd4057&)


Once 8 users have reacted, bot will randomly select an encounter and randomly pick role/jobs for everyone with the standard party composition of:
- 2 TANKS
- 2 HEALERS
- 1 MELEE DPS
- 1 PHYSICAL RANGED DPS
- 1 CASTER DPS
- 1 ANY DPS

No duplicate jobs

![8 users reacted](https://cdn.discordapp.com/attachments/333422790612877323/1331691311727644782/image.png?ex=6793326e&is=6791e0ee&hm=fed956140b4da31818e8a9160071bf6f01d1deda82bebb32b688acc384fad266&)

# **Planned Updates**
### Features
- Include random modifiers for more difficulty
    - Encounter specific 
        - No TANK LB3 in FRU
        - No mariokart strategy in UCoB Grand Octet
        - No Arm's Length/Surecast TEA 
    - General
        - Healer's can't AOE heal
        - Tanks must play with no tank stance
        - No Arm's Length/Surecast
        - No Dots
- User configuration for including/excluding jobs not unlocked or levelled
- Server configuration to include/exclude specific encounters on the list
            


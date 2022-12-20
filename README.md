# Agent-Based Modeling and Social System Simulation 2022

> * Group Name: Duology
> * Group participants names: Nikhil Sethukumar, Vishnu Varadan
> * Project Title: Overcoming Braess's Paradox

## General Introduction

<!-- (States your motivation clearly: why is it important / interesting to solve this problem?)
(Add real-world examples, if any)
(Put the problem into a historical context, from what does it originate? Are there already some proposed solutions?) -->

Braess's Paradox is an unintuitive occurrence in a specific class of congestion games. This reveals the advantages of a model-based approach and promotes mathematical modelling of real-world scenarios. Who would agree if they were told that adding a huge highway could make traffic worse?

> ON Earth Day this year, New York City's Transportation Commissioner decided to close 42d Street, which as every New Yorker knows is always congested. ... But to everyone's surprise, Earth Day generated no historic traffic jam. Traffic flow actually improved when 42d Street was closed. [^nytimes]

[^nytimes]: An excerpt from an article in the 25 Dec 1990 issue of _The New York Times_. 

So we see that the problem is indeed of great relevance. We attempt to solve this problem by allowing cooperation and interaction between the agents.

## The Model

<!-- (Define dependent and independent variables you want to study. Say how you want to measure them.) (Why is your model a good abtraction of the problem you want to study?) (Are you capturing all the relevant aspects of the problem?) -->

We consider a similar problem, in the context of grossing the Grand Canal in Venice. It turns out, when people are allowed to use the bridge to cross and everyone tries to get across as quick as they can, everyone gets later by 5 minutes.

![Venice Rialto crossing](/presentation/images/Venice_bridge_crossing_illustration.png)



## Fundamental Questions

<!-- (At the end of the project you want to find the answer to these questions)
(Formulate a few, clear questions. Articulate them in sub-questions, from the more general to the more specific. ) -->

- Does allowing cooperation between the agents result in a cost lower than the cost without the bridge?
  - How much cooperation is needed?
  - How benevolent do the agents need to be?
- Does changing the neighbors of the agent result in a lower social cost?
  - How many neighbors does an agent need to have for the effect to be noticable?
- Is it possible to have intelligent agents that change their cooperativeness?
  - What rules need to be obeyed by the agents so that the cost can be lowered most?
  - Is it possible to alterate between cooperative states based on history of costs incurred?


## Expected Results

<!-- (What are the answers to the above questions that you expect to find before starting your research?) -->

We expect that the cost decreases with increasing cooperation between the agents. Whether it will be strong enough for the existence of the bridge to show its benefits stands to be seen.

## References 

(Add the bibliographic references you intend to use)
(Explain possible extension to the above models)
(Code / Projects Reports of the previous year)

- Hespanha, Jo ̃ao P.
  Noncooperative Game Theory: An Introduction for Engineers and Computer Scientists. Princeton University Press, 2017. (https://doi.org/10.2307/j.ctt1vwmgbh)
- Helbing, Dirk, Martin Sch ̈onhof, Hans-Ulrich Stark, and Janusz A. Holyst.
  How individuals learn to take turns: Emergence of alternating cooperation in a congestion game and the prisoner’s dilemma.
  Advances in Complex Systems, 8, no. 01 (2005): 87-116.


## Research Methods

Agent-Based Model
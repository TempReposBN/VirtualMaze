﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

/// <summary>
/// Class for encapsulation the data required to parse and unparse settings to be logged into
/// the session Logs.
/// </summary>
[Serializable]
public class SessionContext {
    public string version;
    public string triggerVersion;
    public string taskType;
    public List<PosterLocation> posterLocations = new List<PosterLocation>();
    public string trialName;
    public int rewardsNumber; //number of trials
    public int completionWindow;
    public int timeoutDuration;
    public int intersessionInterval;
    public int rewardTime;
    public int rewardDistance;
    public float rewardViewCriteria;
    public float rotationSpeed;
    public float movementSpeed;
    public float joystickDeadzone;

    public SessionContext(Session session, ExperimentSettings settings, RewardArea[] rewards) {
        version = GameController.versionInfo;
        triggerVersion = GameController.pportInfo;
        taskType = "Continuous";
        trialName = session.level;
        rewardsNumber = session.numTrials;

        foreach (RewardArea reward in rewards) {
            posterLocations.Add(new PosterLocation(reward.target.position, reward.target.name));
        }

        GetJoystickSettings(settings);
        GetRobotMovementSettings(settings);
        GetRewardSettings(settings);
        GetExperimentSettings(settings);
    }

    /// <summary>
    /// Creates a SessionContext with the old header where data is stored line by line
    /// </summary>
    /// <param name="currentline"></param>
    /// <param name="reader"></param>
    public SessionContext(string currentLine, StreamReader reader) {
        string line = currentLine;
        version = GetValue(line);

        line = reader.ReadLine();
        triggerVersion = GetValue(line);

        line = reader.ReadLine();
        taskType = GetValue(line);

        line = reader.ReadLine();//ignore parsing of poster location for now
        //context.posterLocations = GetValue(lin;

        line = reader.ReadLine();
        trialName = GetValue(line);

        line = reader.ReadLine();
        int.TryParse(GetValue(line), out rewardsNumber);

        line = reader.ReadLine();
        int.TryParse(GetValue(line), out completionWindow);

        line = reader.ReadLine();
        int.TryParse(GetValue(line), out timeoutDuration);

        line = reader.ReadLine();
        int.TryParse(GetValue(line), out intersessionInterval);

        line = reader.ReadLine();
        int.TryParse(GetValue(line), out rewardTime);

        line = reader.ReadLine();
        float.TryParse(GetValue(line), out rotationSpeed);

        line = reader.ReadLine();
        float.TryParse(GetValue(line), out movementSpeed);

        line = reader.ReadLine();
        float.TryParse(GetValue(line), out joystickDeadzone);

        line = reader.ReadLine();
        float.TryParse(GetValue(line), out rewardViewCriteria);
    }

    public string ToJsonString() {
        return JsonUtility.ToJson(this, false);
    }

    public string ToJsonString(bool prettyPrint) {
        return JsonUtility.ToJson(this, prettyPrint);
    }

    //helper methods to log required settings
    private void GetJoystickSettings(ExperimentSettings settings) {
        if (settings.TryGetComponentSetting(out JoystickController.Settings joystickSettings)) {
            joystickDeadzone = joystickSettings.deadzoneAmount;
        }
        else {
            //this values are a must to be logged. Therefore an exception is thrown.
            throw new SaveLoad.SettingNotFoundException("JoystickController.Settings not found");
        }
    }

    private void GetRobotMovementSettings(ExperimentSettings settings) {
        if (settings.TryGetComponentSetting(out RobotMovement.Settings movementSettings)) {
            rotationSpeed = movementSettings.rotationSpeed;
            movementSpeed = movementSettings.movementSpeed;
        }
        else {
            //this values are a must to be logged. Therefore an exception is thrown.
            throw new SaveLoad.SettingNotFoundException("RobotMovement.Settings not found");
        }
    }

    private void GetRewardSettings(ExperimentSettings settings) {
        if (settings.TryGetComponentSetting(out RewardsController.Settings rewardSettings)) {
            rewardTime = rewardSettings.rewardDurationMilliSecs;
            rewardViewCriteria = rewardSettings.requiredViewAngle;
        }
        else {
            //this values are a must to be logged. Therefore an exception is thrown.
            throw new SaveLoad.SettingNotFoundException("RewardsController.Settings not found");
        }
    }

    private void GetExperimentSettings(ExperimentSettings settings) {
        if (settings.TryGetComponentSetting(out ExperimentController.Settings experimentSettings)) {
            completionWindow = experimentSettings.timeLimitDuration;
            timeoutDuration = experimentSettings.timeoutDuration;
            intersessionInterval = experimentSettings.sessionIntermissionDuration;
        }
        else {
            //this values are a must to have. Therefore an exception is thrown
            throw new SaveLoad.SettingNotFoundException("ExperimentController.Settings not found");
        }
    }

    private string GetValue(string line) {
        //get second index where the value resides
        return line.Split(':')[1].Trim();
    }

    [Serializable]
    public struct PosterLocation {
        public string name;
        public Vector3 position;
        public PosterLocation(Vector3 position, string name) {
            this.name = name;
            this.position = position;
        }
    }
}
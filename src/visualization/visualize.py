import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df["set"] == 1]
plt.plot(set_df["acc_y"])
plt.plot(set_df["acc_y"].reset_index(drop=True))
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df["label"].unique():
    subset = df[df["label"]==label]
    fig, ax = plt.subplots()
    plt.plot(set_df["acc_y"].reset_index(drop=True), label = label)
    plt.legend()
    plt.show()

for label in df["label"].unique():
    subset = df[df["label"]==label]
    fig, ax = plt.subplots()
    plt.plot(set_df[:100]["acc_y"].reset_index(drop=True), label = label)
    plt.legend()
    plt.show()
# --------------------------------------------------------------
    #https://docs.datalumina.io/ccQSzikoeMmqZE
# Adjust plot settings
# https://docs.datalumina.io/ccQSzikoeMmqZE/b/3BF4A636-FB3A-4C6F-B588-90EF5B4EF219/Customizing-Matplotlib-with-style-sh--------------------------------------------------------------
    
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20,5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------

category_df = df.query("category == 'squat'").query("label =='A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
participiant_df = df.query("category == 'bench'").sort_values("label").reset_index()

fig, ax = plt.subplots()
participiant_df.groupby(["label"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

participiant_df['participant'].value_counts()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
category = "squat"
label = "A"

all_axis_df = df.query(f"category == '{category}'").query(f"label =='{label}'").reset_index()
fig, ax = plt.subplots()
all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
categories = df["category"].unique()
labels = df['label'].unique()
for category in categories:
    for label in labels:
        all_axis_df = (
            df.query(f"category == '{category}'").query(f"label =='{label}'").reset_index()
        )

        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
         #   all_axis_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax)
         #   ax.set_ylabel("gyr_y")
            ax.set_xlabel("samples")
            plt.title(f"{label}({participant})".title())
            plt.legend()

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
category = "row"
label = "A"

combined_plot_df = (
    df.query(f"category == '{category}'").query(f"label =='{label}'").reset_index(drop=True)
    )

fig, ax = plt.subplots(nrows=2, sharex = True, figsize=(20,10))
combined_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
combined_plot_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax[1])
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5,1.15), ncol = 3, fancybox = True, shadow = True)

ax[1].legend(loc="upper center", bbox_to_anchor=(0.5,1.15), ncol = 3, fancybox = True, shadow = True)
ax[1].set_xlabel("samples")

# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
categories = df["category"].unique()
labels = df['label'].unique()
for category in categories:
    for label in labels:
        combined_plot_df = (
            df.query(f"category == '{category}'").query(f"label =='{label}'").reset_index()
        )

        if len(combined_plot_df) > 0:
            fig, ax = plt.subplots(nrows=2, sharex = True, figsize=(20,10))
            combined_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
            combined_plot_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax[1])
            ax[0].legend(loc="upper center", bbox_to_anchor=(0.5,1.15), ncol = 3, fancybox = True, shadow = True)

            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5,1.15), ncol = 3, fancybox = True, shadow = True)
            ax[1].set_xlabel("samples")
            #plt.savefig(f"../../reports/figures/{category.title()} ({label}).png")
            plt.show()

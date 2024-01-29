module load cuda/cuda-11.2.0-intel-19.0.4-tn4edsz
module add ffmpeg/4.2.2-intel-19.0.4-getxwtz
export PYTHONPATH=/auto/brno2/home/xjurca08/python_env/usr/local/lib/python3.9/dist-packages/:$PYTHONPATH
export PATH=/auto/brno2/home/xjurca08/python_env/usr/local/bin/:$PATH
export LD_LIBRARY_PATH=/auto/brno2/home/xjurca08/python_env/usr/local/lib:${LD_LIBRARY_PATH}
export HF_DATASETS_CACHE=$SCRATCHDIR/hf_cache
export PATH=$PATH:/storage/brno2/home/xjurca08/.local/bin

LANG=en
cd /storage/brno2/home/xjurca08/storage/brno2/home/xjurca08/spelling



python3.9 run_summarization.py \
    --model_name_or_path google/mt5-small \
    --do_train \
    --do_eval \
    --train_file /auto/brno12-cerit/home/xjurca08/prepared/$LANG/$LANG.train.csv \
    --validation_file /auto/brno12-cerit/home/xjurca08/prepared/$LANG/$LANG.test.csv \
    --output_dir $(pwd)/$LANG/ \
    --overwrite_output_dir \
    --source_prefix "correct: " \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=16 \
    --gradient_accumulation_steps=4 \
    --predict_with_generate \
	--logging_steps="10" \
    --save_total_limit="2" \
    --learning_rate="3e-4" \
    --max_target_length=1024 \
    --max_source_length=1024 \
    --push_to_hub True \
    --hub_model_id "jjurca/mt5-spelling-$LANG-small" \
    --hub_token "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" \
    --run_name "mt5-spelling-$LANG-small" 
